# -*- coding: utf-8 -*-
"""
Created on Sat May 23 14:28:22 2015

@author: Wall-e
"""

import pylab


class RealTimePlotter:
    def __init__(self, ang, signal_femoral, signal_gastrocnemius, filtered_speed, angSpeed, controlSignal,
                 angSpeedRefHistory, errorHistory, xRange, running):
        ####################################
        # Grafico
        self.xRange = xRange
        xAchse = pylab.arange(0, self.xRange, 1)
        yAchse = pylab.array([0] * self.xRange)

        fig = pylab.figure(1, figsize=(13, 10))
        self.ax = fig.add_subplot(511)
        self.ax.grid(True)
        self.ax.set_title("Real time Cycling Plot")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("Angle")
        self.ax.axis([0, self.xRange, -1.5, 1.5])
        self.line1 = self.ax.plot(xAchse, yAchse, '-')

        self.ax2 = fig.add_subplot(512)
        self.ax2.grid(True)
        self.ax2.set_title("")
        self.ax2.set_xlabel("")
        self.ax2.set_ylabel("Stimulation")
        self.ax2.axis([0, self.xRange, -1.5, 1.5])
        self.line2 = self.ax2.plot(xAchse, yAchse, '-')
        self.line3 = self.ax2.plot(xAchse, yAchse, '-')

        self.ax3 = fig.add_subplot(513)
        self.ax3.grid(True)
        self.ax3.set_title("")
        self.ax3.set_xlabel("")
        self.ax3.set_ylabel("Speed")
        self.ax3.axis([0, self.xRange, -1.5, 1.5])
        self.line4 = self.ax3.plot(xAchse, yAchse, '-')
        self.line5 = self.ax3.plot(xAchse, yAchse, '-')
        self.line6 = self.ax3.plot(xAchse, yAchse, '-')

        self.ax4 = fig.add_subplot(514)
        self.ax4.grid(True)
        self.ax4.set_title("")
        self.ax4.set_xlabel("")
        self.ax4.set_ylabel("Control")
        self.ax4.axis([0, self.xRange, -1.5, 1.5])
        self.line7 = self.ax4.plot(xAchse, yAchse, '-')

        self.ax5 = fig.add_subplot(515)
        self.ax5.grid(True)
        self.ax5.set_title("")
        self.ax5.set_xlabel("Time")
        self.ax5.set_ylabel("Error")
        self.ax5.axis([0, self.xRange, -1.5, 1.5])
        self.line8 = self.ax5.plot(xAchse, yAchse, '-')

        self.manager = pylab.get_current_fig_manager()

        self.timer = fig.canvas.new_timer(interval=10)
        self.timer.add_callback(self.plotter, ang, signal_femoral, signal_gastrocnemius, filtered_speed, angSpeed,
                                controlSignal, angSpeedRefHistory, errorHistory, running)
        self.timer.start()

        pylab.show()

    ####################################

    def plotter(self, ang, signal_femoral, signal_gastrocnemius, filtered_speed, angSpeed, controlSignal,
                angSpeedRefHistory, errorHistory, running):
        if not running:
            self.timer.stop()

        CurrentXAxis = pylab.arange(len(ang) - self.xRange, len(ang), 1)

        self.line1[0].set_data(CurrentXAxis, pylab.array(ang[-self.xRange:]))
        self.line2[0].set_data(CurrentXAxis, pylab.array(signal_femoral[-self.xRange:]))
        self.line3[0].set_data(CurrentXAxis, pylab.array(signal_gastrocnemius[-self.xRange:]))
        self.line4[0].set_data(CurrentXAxis, pylab.array(filtered_speed[-self.xRange:]))
        self.line5[0].set_data(CurrentXAxis, pylab.array(angSpeed[-self.xRange:]))
        self.line6[0].set_data(CurrentXAxis, pylab.array(angSpeedRefHistory[-self.xRange:]))
        self.line7[0].set_data(CurrentXAxis, pylab.array(controlSignal[-self.xRange:]))
        self.line8[0].set_data(CurrentXAxis, pylab.array(errorHistory[-self.xRange:]))

        self.ax.axis([CurrentXAxis.min(), CurrentXAxis.max(), -5, 365])
        self.ax2.axis([CurrentXAxis.min(), CurrentXAxis.max(), -0.2, 1.2])
        self.ax3.axis([CurrentXAxis.min(), CurrentXAxis.max(), -5, 450])
        self.ax4.axis([CurrentXAxis.min(), CurrentXAxis.max(), -1.1, 1.1])
        self.ax5.axis([CurrentXAxis.min(), CurrentXAxis.max(), -100, 100])

        self.manager.canvas.draw()


        ####################################
