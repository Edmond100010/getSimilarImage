import cv2 as cv
import os, sys
import numpy as np
import pandas as pd
import shutil



based_path = "Based"

based_list = []
def getDifferent(matrix1, matrix2):
    score = 0
    for i in range (0, len(matrix1)):
        score = score + abs(matrix1[i] - matrix2[i])
    return score


def getBasedPath(df_MVLP):
    for file in os.listdir(based_path):
        angle =int(file.split("_")[0])
        based_angleimagePath = os.path.join(based_path,file)
        for based_angleimage in os.listdir(based_angleimagePath):
            id = int(based_angleimage)
            gender = df_MVLP.loc[df_MVLP.ID == id,'gender'].values[0]
            init_count = 0 
            init_basedimage = [0 for i in range(3)]
            based_imagefolderPath = os.path.join(based_angleimagePath,based_angleimage)
            for based_image in os.listdir(based_imagefolderPath):
                based_image = os.path.join(based_imagefolderPath,based_image)
                init_basedimage[init_count] = based_image
                init_count += 1
            based_list.append([angle, gender, init_basedimage[0], init_basedimage[1]])
    return(based_list)

def save(path,filename):
    a = path.split("\\")
    dest_fpath = "%s/%s/%s/%s"%("Pick",a[1],a[2],a[3])
    os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
    save_path = "%s/%s/%s/%s"%("Pick",a[1],a[2],filename)
    shutil.copyfile(path, save_path)

def norm_diff(based_list, df_MVLP):
    path = "MVLP_StanceSwing"
    for file in os.listdir(path):
        angle = int(file.split("_")[1].split("-")[0])
        imganglefolder_path = os.path.join(path,file)
        for image_folder in os.listdir(imganglefolder_path):
            init_stance = [0 for i in range (3)]
            init_swing = [0 for i in range (3)]
            image_path = os.path.join(imganglefolder_path,image_folder)
            id = int(image_folder)
            gender = df_MVLP.loc[df_MVLP.ID == id,'gender'].values[0]
            for image in os.listdir(image_path):
                total_stancescore = 0
                total_swingscore = 0
                gei_path = os.path.join(image_path,image)
                image_num = (int(image[:-4]))
                for i in based_list:
                    if(i[0] == angle):
                        if(i[1] == gender):
                            gei = cv.imread(gei_path)
                            height, width = 960, 1280
                            based_stancegei = cv.imread(i[2])
                            errorstanceL2 = cv.norm( gei, based_stancegei, cv.NORM_L2 )
                            similarity_stance = 1 - errorstanceL2 / ( height * width )
                            total_stancescore = total_stancescore + similarity_stance
                            based_swinggei = cv.imread(i[3])                            
                            errorswingL2 = cv.norm( gei, based_swinggei, cv.NORM_L2 )
                            similarity_swing = 1 - errorswingL2 / ( height * width )
                            total_swingscore = total_swingscore + similarity_swing
                if total_stancescore > init_stance[0]:
                    init_stance[0] = total_stancescore
                    init_stance[1] = gei_path
                    init_stance[2] = image_num
                    init_swing = [0 for i in range (3)]

                if total_swingscore > init_swing[0]:
                        init_swing[0] = total_swingscore
                        init_swing[1] = gei_path
            save(init_stance[1], "stance.png")
            save(init_swing[1], "swing.png")
            print(init_swing[1], end = "\r")



def main():
    df_MVLP = pd.read_csv('subject_info_OUMVLP.csv')
    based_list = getBasedPath(df_MVLP)
    norm_diff(based_list, df_MVLP)
if __name__ == "__main__":
    main()
