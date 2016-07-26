# -*- coding: utf-8 -*-
"""
Created on Sat May 23 14:28:22 2015

@author: Wall-e
"""

import pylab


class RealTimePlotter:
    def __init__(self, ang, signal_0, signal_1, signal_2, signal_3, signal_4, signal_5, filtered_speed, angSpeed, controlSignal,
                 angSpeedRefHistory, errorHistory, xRange):
        ####################################
        # Grafico
        self.xRange = xRange
        xAchse = pylab.arange(0, self.xRange, 1)
        yAchse = pylab.array([0] * self.xRange)

        fig = pylab.figure(1, figsize=(13, 10))
        self.ax = fig.add_subplot(611)
        self.ax.grid(True)
        self.ax.set_title("Real time Cycling Plot")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("Angle")
        self.ax.axis([0, self.xRange, -1.5, 1.5])
        self.line1 = self.ax.plot(xAchse, yAchse, '-')

        self.ax2 = fig.add_subplot(612)
        self.ax2.grid(True)
        self.ax2.set_title("")
        self.ax2.set_xlabel("")
        self.ax2.set_ylabel("Left leg")
        self.ax2.axis([0, self.xRange, -1.5, 1.5])
        self.line2q = self.ax2.plot(xAchse, yAchse, '-')
        self.line2h = self.ax2.plot(xAchse, yAchse, '-')
        self.line2g = self.ax2.plot(xAchse, yAchse, '-')

        self.ax2r = fig.add_subplot(613)
        self.ax2r.grid(True)
        self.ax2r.set_title("")
        self.ax2r.set_xlabel("")
        self.ax2r.set_ylabel("Right leg")
        self.ax2r.axis([0, self.xRange, -1.5, 1.5])
        self.line3q = self.ax2r.plot(xAchse, yAchse, '-')
        self.line3h = self.ax2r.plot(xAchse, yAchse, '-')
        self.line3g = self.ax2r.plot(xAchse, yAchse, '-')

        self.ax3 = fig.add_subplot(614)
        self.ax3.grid(True)
        self.ax3.set_title("")
        self.ax3.set_xlabel("")
        self.ax3.set_ylabel("Speed")
        self.ax3.axis([0, self.xRange, -1.5, 1.5])
        self.line4 = self.ax3.plot(xAchse, yAchse, '-')
        self.line5 = self.ax3.plot(xAchse, yAchse, '-')
        self.line6 = self.ax3.plot(xAchse, yAchse, '-')

        self.ax4 = fig.add_subplot(615)
        self.ax4.grid(True)
        self.ax4.set_title("")
        self.ax4.set_xlabel("")
        self.ax4.set_ylabel("Control")
        self.ax4.axis([0, self.xRange, -1.5, 1.5])
        self.line7 = self.ax4.plot(xAchse, yAchse, '-')

        self.ax5 = fig.add_subplot(616)
        self.ax5.grid(True)
        self.ax5.set_title("")
        self.ax5.set_xlabel("Time")
        self.ax5.set_ylabel("Error")
        self.ax5.axis([0, self.xRange, -1.5, 1.5])
        self.line8 = self.ax5.plot(xAchse, yAchse, '-')

        self.manager = pylab.get_current_fig_manager()

        self.timer = fig.canvas.new_timer(interval=10)
        self.timer.add_callback(self.plotter, ang, signal_0, signal_1, signal_2, signal_3, signal_4, signal_5, filtered_speed, angSpeed,
                                controlSignal, angSpeedRefHistory, errorHistory)
        self.timer.start()

        # pylab.show(block=False)
        pylab.show()

    ####################################

    def plotter(self, ang, signal_0, signal_1, signal_2, signal_3, signal_4, signal_5, filtered_speed, angSpeed, controlSignal,
                angSpeedRefHistory, errorHistory):

        CurrentXAxis = pylab.arange(len(ang) - self.xRange, len(ang), 1)

        self.line1[0].set_data(CurrentXAxis, pylab.array(ang[-self.xRange:]))
        self.line2q[0].set_data(CurrentXAxis, pylab.array(signal_0[-self.xRange:]))
        self.line2h[0].set_data(CurrentXAxis, pylab.array(signal_1[-self.xRange:]))
        self.line2g[0].set_data(CurrentXAxis, pylab.array(signal_2[-self.xRange:]))
        self.line3q[0].set_data(CurrentXAxis, pylab.array(signal_3[-self.xRange:]))
        self.line3h[0].set_data(CurrentXAxis, pylab.array(signal_4[-self.xRange:]))
        self.line3g[0].set_data(CurrentXAxis, pylab.array(signal_5[-self.xRange:]))
        self.line4[0].set_data(CurrentXAxis, pylab.array(filtered_speed[-self.xRange:]))
        self.line5[0].set_data(CurrentXAxis, pylab.array(angSpeed[-self.xRange:]))
        self.line6[0].set_data(CurrentXAxis, pylab.array(angSpeedRefHistory[-self.xRange:]))
        self.line7[0].set_data(CurrentXAxis, pylab.array(controlSignal[-self.xRange:]))
        self.line8[0].set_data(CurrentXAxis, pylab.array(errorHistory[-self.xRange:]))

        self.ax.axis([CurrentXAxis.min(), CurrentXAxis.max(), -5, 365])
        self.ax2.axis([CurrentXAxis.min(), CurrentXAxis.max(), -0.2, 1.2])
        self.ax2r.axis([CurrentXAxis.min(), CurrentXAxis.max(), -0.2, 1.2])
        self.ax3.axis([CurrentXAxis.min(), CurrentXAxis.max(), -5, 450])
        self.ax4.axis([CurrentXAxis.min(), CurrentXAxis.max(), -1.1, 1.1])
        self.ax5.axis([CurrentXAxis.min(), CurrentXAxis.max(), -100, 100])

        self.manager.canvas.draw()


        ####################################

    def stop_timer(self):
        self.timer.stop()

    def start_timer(self):
        self.timer.start()
