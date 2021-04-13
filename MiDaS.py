import os
import cv2
import argparse
import numpy as np

from time import time
from pathlib import Path

import utils

class MiDas:
    def __init__(self):
        self.names = []
        # Read Network
        p = str(Path('.').absolute())
        # MiDaS v2.1 Small
        self.net = cv2.dnn.readNet(p + '/model-small.onnx')
        # Set Preferable Backend and Target
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def get_inference(self, img, normalize):
        # Create Blob from Input Image
        # MiDaS v2.1 Small ( Scale : 1 / 255, Size : 256 x 256, Mean Subtraction : ( 123.675, 116.28, 103.53 ), Channels Order : RGB )
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (256, 256), (123.675, 116.28, 103.53), True, False )
        # Set Input Blob
        self.net.setInput(blob)
        # Run Forward Network
        output = self.net.forward(self.__get_outputs_names(self.net)[0])
        # Convert Size to 256x256 from 1x256x256
        output = np.squeeze(output, axis=0)
        output = cv2.resize(output, (img.shape[1], img.shape[0]))

        if normalize:
            output = cv2.normalize(output, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        else:
            output = np.uint8(output/8)
        return output

    def __get_outputs_names(self, net):
        if len(self.names) == 0:
            out_layers = net.getUnconnectedOutLayers()
            layers_names = net.getLayerNames()

            for out_layer in out_layers:
                self.names.append(layers_names[out_layer[0] - 1])
        return self.names

def main(opt):
    # Open Video Capture
    if opt.rpi_cam:
        cap = utils.RPI_Video()
    else:
        cap = cv2.VideoCapture(0)
        cap.set(3,320)
        cap.set(4,240)

    # Read Frame
    _, input = cap.read()

    MD = MiDas()
    tps = utils.PerfTools()

    if opt.save is not None:
        os.makedirs(opt.save, exist_ok=True)

    try:
        while True:
            tps.start()
            # Read Frame
            _, input = cap.read()

            output = MD.get_inference(input, opt.normalize)

            print(tps.end_hz())

            if opt.no_output:
                cv2.imshow('pred', output)
                cv2.waitKey(1)
            if opt.save is not None:
                sname = opt.save + '/' + utils.save_name() + '.png'
                cv2.imwrite(sname, output)

    except KeyboardInterrupt:
        print(str(round(tps.get_average_hz(), 2)) + " Hz")
        cap.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", default=None, help="specify a name to save images", action="store", type=str)
    parser.add_argument("--rpi_cam", help="use the raspberry pi camera", action="store_true")
    parser.add_argument("--no_output", help="disabling video output", action="store_false")
    parser.add_argument("--normalize", help="normalize the output", action="store_true")
    args = parser.parse_args()

    main(parser.parse_args())
