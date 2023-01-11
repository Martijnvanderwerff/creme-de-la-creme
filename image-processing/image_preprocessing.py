from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import yaml
import rawpy
import os
import seaborn as sns
import cv2 as cv

NEFS_PATH = "NEFs"
JPEGS_PATH = "JPEGs"
JPEGS_CROPPED_PATH = "JPEGs_cropped"
HISTS_PATH = "JPEGs_hists"
JPEGS_NORM_PATH = "JPEGs_norm"
HISTS_NORM_PATH = "JPEGs_hists_norm"
JPEGS_NORM_THRESHOLD_PATH = "JPEGs_norm_thresholded"
PROJECT_PATH = "../Photo-data"
PATIENT_NAMES = ['Patient1', 'Patient2', 'Patient3', 'Patient4', 'Patient5', 'Patient6']
PHOTOS_AMOUNT_PER_PERSON = 6


def get_config():
    with open("config.yaml", 'r') as stream:
        config_from_file = yaml.safe_load(stream)
    return config_from_file


config = get_config()
DATA_FOLDERS = (config['datapaths'])
if not isinstance(DATA_FOLDERS, list):
    raise Exception('datapaths field in config should be list of directories')


def getSeabornHostogram(img1, img2, color1='red', color2='blue', title='Comparison of red channels', file_name='hist1'):
    sns.set_theme(style="darkgrid")

    sns.histplot(data=img1[:, :, 0].ravel(), bins=100, color=color1, label="img1", kde=True, multiple="stack")
    sns.histplot(data=img2[:, :, 0].ravel(), bins=100, color=color2, label="img2", kde=True, multiple="stack")

    plt.title(title)
    plt.legend(loc='upper right')
    plt.savefig(file_name)
    plt.clf()


def saveRedChannelWithFilteredPixels(img, left, right, file_name):
    if left < 0 or right > 255 or (not file_name.endswith('.png')) or len(img.shape) != 3:
        raise Exception(
            "Left border should be more than 0, right border should be less than 256, file_name should be of .png type")
    img = img[:, :, 0]
    reddish = (img[:, :] < right) & (img[:, :] > left)
    img[reddish] = 0
    io.imsave(file_name, img)


def makeDirectoryForJPEGs(path):
    if not os.path.isdir(path):
        os.mkdir(path)
        return
    if len(os.listdir(path)) > 0:
        raise Exception(path + " directory is not empty")


def convert_NEFs_to_JPEGs(folder_path):
    if not os.path.isdir(folder_path) or len(os.listdir(folder_path)) == 0:
        raise Exception("Directory " + folder_path + " doesn't exist or is empty")
    found_slash = folder_path.strip('/').rindex('/')
    jpegs_dir_path = os.path.join(folder_path[:found_slash], JPEGS_PATH)
    makeDirectoryForJPEGs(jpegs_dir_path)

    counter = 1
    files = os.listdir(folder_path)
    for path in files:
        print("processing[convert nefs to jpegs]: ", counter, "/", len(files))
        counter += 1
        file_path = os.path.join(folder_path, path)
        if os.path.isfile(file_path):
            with rawpy.imread(file_path) as raw:
                rgb = raw.postprocess()
                io.imsave(os.path.join(jpegs_dir_path, path) + '.jpg', rgb)


def rightSideFilter(height, width):
    return width * 5, width * 7, height * 9, height * 11


def leftSideFilter(height, width):
    return width * 9, width * 11, height * 9, height * 11


# filter for left side (last three images of six per person) and filter for right side (first three images of six per person) are different
def cropImage(img, file_name, leftSide):
    params = img.shape
    l = int(params[0] / 16)
    w = int(params[1] / 16)
    if leftSide:
        left_border, right_border, bottom_border, top_border = leftSideFilter(l, w)
    else:
        left_border, right_border, bottom_border, top_border = rightSideFilter(l, w)
    img_cropped = img[bottom_border:top_border, left_border:right_border]
    io.imsave(file_name, img_cropped)


def sortFileInFolder(folder):
    listedDir = os.listdir(folder)
    if not os.path.isdir(folder) or len(listedDir) == 0:
        raise Exception("Directory " + folder + " doesn't exist or is empty")
    return sorted(filter(lambda x: os.path.isfile(os.path.join(folder, x)), listedDir))


# automatically cropping the pictures
def crop_JPEGs(folder_path):
    files = sortFileInFolder(folder_path)
    found_slash = folder_path.strip('/').rindex('/')
    jpegs_dir_path = os.path.join(folder_path[:found_slash], JPEGS_CROPPED_PATH)
    makeDirectoryForJPEGs(jpegs_dir_path)

    counter = 0
    for path in files:
        print("processing[crop jpegs]: ", counter + 1, "/", len(files))
        counter += 1
        file_path = os.path.join(folder_path, path)
        if os.path.isfile(file_path):
            img = plt.imread(file_path)
            cropImage(img, os.path.join(jpegs_dir_path, path) + '_cropped.jpg', ((counter - 1) % 6) > 2)


def getBordersOfDataSetsPerPerson():
    patient_photosets = {}
    counter = 0
    for patient in PATIENT_NAMES:
        patient_photosets[patient] = (PHOTOS_AMOUNT_PER_PERSON * counter, PHOTOS_AMOUNT_PER_PERSON * (counter + 1))
        counter += 1
    return patient_photosets


patient_photosets = getBordersOfDataSetsPerPerson()

def compareTwoDataSetsWithHistograms(folder1, folder2, hists_folder):
    files_dir1 = sortFileInFolder(folder1)
    files_dir2 = sortFileInFolder(folder2)
    makeDirectoryForJPEGs(hists_folder)
    if len(files_dir1) != len(files_dir2):
        raise Exception("Directories " + folder1 + " and " + folder2 + " contain different amounts of files")
    for name, borders in patient_photosets.items():
        print("processing[build hist: right side]: ", name)
        img_orig1, img_orig2 = io.imread(os.path.join(folder1, files_dir1[borders[0]])), io.imread(
            os.path.join(folder2, files_dir2[borders[0]]))
        getSeabornHostogram(img_orig1, img_orig2, file_name=os.path.join(hists_folder, name + "_right"),
                            title=name + ": right side")


def normalizePictures(fromFolder, toFolder):
    files_dir = sortFileInFolder(fromFolder)
    makeDirectoryForJPEGs(toFolder)
    counter = 0
    for path in files_dir:
        print("processing[normalize jpegs]: ", counter + 1, "/", len(files_dir))
        counter += 1
        file_path = os.path.join(fromFolder, path)
        if os.path.isfile(file_path):
            img = cv.imread(file_path)
            norm_img = np.zeros((img.shape[0], img.shape[1]))
            final_img = cv.normalize(img, norm_img, 0, 255, cv.NORM_MINMAX)
            cv.imwrite(os.path.join(toFolder, path + "_norm.jpg"), final_img)


# create image where certain pixels (according to the filter) on red channel are set to 0 (black)
def thresholdPictures(fromFolder, toFolder):
    files_dir = sortFileInFolder(fromFolder)
    makeDirectoryForJPEGs(toFolder)
    counter = 0
    for path in files_dir:
        print("processing[threshold jpegs]: ", counter + 1, "/", len(files_dir))
        counter += 1
        file_path = os.path.join(fromFolder, path)
        if os.path.isfile(file_path):
            img = io.imread(file_path)
            img_red = img[:, :, 0]
            mean = np.mean(img_red)

            # should define certain threshold for every person and every side differently
            saveRedChannelWithFilteredPixels(img, int(mean) - 30, int(mean),
                                             os.path.join(toFolder, path + "_thresholded.png"))


# convert all datasets pictures to jpeg format, crop them automatically, normalize and threshold
for i in range(0, len(DATA_FOLDERS)):
    folder_path = os.path.join(PROJECT_PATH, DATA_FOLDERS[i], NEFS_PATH)
    convert_NEFs_to_JPEGs(folder_path)
    crop_path = os.path.join(PROJECT_PATH, DATA_FOLDERS[i], JPEGS_PATH)
    crop_JPEGs(crop_path)
    normalizePictures(os.path.join(PROJECT_PATH, DATA_FOLDERS[i], JPEGS_CROPPED_PATH),
                      os.path.join(PROJECT_PATH, DATA_FOLDERS[i], JPEGS_NORM_PATH))
    thresholdPictures(os.path.join(PROJECT_PATH, DATA_FOLDERS[i], JPEGS_NORM_PATH),
                      os.path.join(PROJECT_PATH, DATA_FOLDERS[i], JPEGS_NORM_THRESHOLD_PATH))


# is used to detect the shifts of images taken in different days, resulting histograms show that automatically
# cropping method captures shifted areas what is unacceptable for comparing the pictures
def buildHistogramsOfRedChannelValuesDistribution(normalized):
    if normalized:
        jpegs_cropped_path = JPEGS_CROPPED_PATH
        hists_path = HISTS_PATH
    else:
        jpegs_cropped_path = JPEGS_NORM_PATH
        hists_path = HISTS_NORM_PATH

    for i in range(0, len(DATA_FOLDERS) - 1):
        folder_base_line = os.path.join(PROJECT_PATH, DATA_FOLDERS[i], jpegs_cropped_path)
        folder = os.path.join(PROJECT_PATH, DATA_FOLDERS[i + 1], jpegs_cropped_path)
        hists_folder = os.path.join(PROJECT_PATH, DATA_FOLDERS[i + 1], hists_path)
        compareTwoDataSetsWithHistograms(folder_base_line, folder, hists_folder)


# compare pictures of week #n and week #n+1, build histograms of red pixel values distribution
buildHistogramsOfRedChannelValuesDistribution(False)
# compare normalized pictures of week #n and week #n+1, build histograms of red pixel values distribution
buildHistogramsOfRedChannelValuesDistribution(True)

