import os
import cv2
import glob
import argparse
import sys

def encontrar_arquivos_mkv(diretorio):
    """ Encontra todos os arquivos .mkv de forma recursiva em um diretório. """
    return glob.glob(os.path.join(diretorio, '**/*.mkv'), recursive=True)

def contar_frames_video(arquivo):
    """ Conta o número de frames de um vídeo usando OpenCV. """
    cap = cv2.VideoCapture(arquivo)
    if not cap.isOpened():
        return 0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frame_count

def obter_quantidade_frames_por_video(diretorio):
    """ Obtém a quantidade de frames por vídeo e exibe na tela. """
    arquivos_mkv = encontrar_arquivos_mkv(diretorio)
    total_frames = 0
    
    for arquivo in arquivos_mkv:
        frame_count = contar_frames_video(arquivo)
        nome_arquivo = os.path.basename(arquivo)
        print(f'{nome_arquivo}: {frame_count} frames')
        total_frames += frame_count
    
    print(f'TOTAL DE FRAMES: {total_frames}')

def main():
    parser = argparse.ArgumentParser(description='Contagem de frames de vídeos .mkv em um diretório.')
    parser.add_argument('diretorio', help='Diretório contendo vídeos .mkv')
    args = parser.parse_args()
    
    diretorio_videos = args.diretorio
    obter_quantidade_frames_por_video(diretorio_videos)

if __name__ == '__main__':
    main()