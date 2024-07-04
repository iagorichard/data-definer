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

def obter_quantidade_frames_por_video(diretorio, skip_check):
    """ Obtém a quantidade de frames por vídeo e exibe na tela. """
    arquivos_mkv = encontrar_arquivos_mkv(diretorio)
    total_frames = 0
    
    for arquivo in arquivos_mkv:
        frame_count = contar_frames_video(arquivo)
        nome_arquivo = os.path.basename(arquivo)
        print(f'{nome_arquivo}: {frame_count} frames')
        total_frames += frame_count
    
    print(f'TOTAL DE FRAMES: {total_frames}')
    print(f"Com frame SKIP de {skip_check}: {total_frames/skip_check}")

def main():
    if len(sys.argv) < 3 or '--diretorio' not in sys.argv:
        print("Uso: python script.py --diretorio <diretório> [--skip_check <numero>]")
        sys.exit(1)
    
    diretorio_idx = sys.argv.index('--diretorio')
    diretorio_videos = sys.argv[diretorio_idx + 1]
    
    skip_check = False
    skip_check_idx = sys.argv.index('--skip_check') if '--skip_check' in sys.argv else -1
    if skip_check_idx != -1:
        skip_check_value = sys.argv[skip_check_idx + 1]
        try:
            skip_check = int(skip_check_value)
        except ValueError:
            print("O valor para skip_check deve ser um número inteiro.")
            sys.exit(1)
    
    obter_quantidade_frames_por_video(diretorio_videos, skip_check)

if __name__ == '__main__':
    main()