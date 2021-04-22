#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import itemgetter #for sorting
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import subprocess
import time
import sys
import os

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.test_mac = ''
        self.ip = ''
        self.test_essid = ''
        self.new_ip = ''
        self.response = ''
        self.setGeometry(400, 100, 500, 500)
        self.setWindowTitle('Wi-Fi Scanner')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        lay = QVBoxLayout(self) # main layout
        self.top_widget = QWidget()
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.top_widget)
        self.vbox = QVBoxLayout()
        self.settings_button = QPushButton("Настройки")
        self.settings_button.setFixedWidth(100)
        self.settings_button.clicked.connect(self.show_settings)
        self.top_widget.setLayout(self.vbox)
        lay.addWidget(self.scroll)
        lay.addWidget(self.settings_button)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(3000)  # milliseconds
        self.timer.timeout.connect(self.scan)
        self.show()
        self.scan()

    def add_lay(self, aps):
        self.ip = ''
        ssid = 'SSID: ' + aps['ESSID']
        mac = aps['MAC']
        channel = 'Channel: ' + aps['Channel']
        power = aps['Power']
        try:
            sequrity = aps['Sequrity']
        except:
            sequrity = '           '
        self.dB_to_percent = 110 - int(power[1:-4])
        self.group = QGroupBox(ssid)
        self.group.setStyleSheet('QGroupBox {font-size: 13px;   font-weight: bold;}')
        self.group.setFixedHeight(100)
        self.cell_vbox = QVBoxLayout()
        self.cell_hbox2 = QHBoxLayout()
        self.cell_hbox3 = QHBoxLayout()
        ip_label = QLabel()
        ip_label.setText('')
        try:
            if (aps['MAC'][:-2].upper() == self.test_mac[:-2].upper()) and (self.response != None):
                self.ip = self.new_ip
                ip_label.setText(self.ip)
                ip_label.setFont(QtGui.QFont('Arial', 10, weight=QtGui.QFont.Bold))
                ip_label.setStyleSheet('QLabel { color : #43ad58; }')

            else:
                self.ip = ''
                ip_label.setText(self.ip)
        except:
            pass

        mac_label = QLabel(mac)
        channel_label = QLabel(channel)
        sequrity_label = QLabel(sequrity)
        mode_label = QLabel(aps['Frequency'])
        self.progr = QProgressBar()
        self.progr.setValue(self.dB_to_percent)
        self.progr.setFormat(power)
        self.progr.setAlignment(Qt.AlignCenter)
        if self.dB_to_percent > 60:
            self.progr.setStyleSheet("QProgressBar {height: 7px;}"
                                     "QProgressBar::chunk "
                                     "{background-color:  #43ad58 ;"
                                     "}")
        if self.dB_to_percent < 30:
            self.progr.setStyleSheet("QProgressBar {height: 7px;}"
                                     "QProgressBar::chunk "
                                     "{background-color: #AF291E;"
                                     "}")
        if (self.dB_to_percent >= 30) and (self.dB_to_percent <= 60):
            self.progr.setStyleSheet("QProgressBar {height: 7px;}"
                                     "QProgressBar::chunk "
                                     "{background-color: #D5CC0C ;"
                                     "}")
        self.progr.setFont(QtGui.QFont('Arial', 10))
        self.cell_hbox1 = QHBoxLayout()
        self.cell_hbox1.addWidget(ip_label)
        self.cell_hbox1.addStretch(10000)
        self.cell_hbox1.addWidget(self.progr)
        self.cell_vbox.addLayout(self.cell_hbox1)
        self.cell_hbox2.addWidget(mac_label)
        self.cell_hbox2.addStretch(1)
        self.cell_hbox2.addWidget(sequrity_label)
        self.cell_hbox3.addWidget(channel_label)
        self.cell_hbox3.addStretch(1)
        self.cell_hbox3.addWidget(mode_label)
        self.cell_vbox.addLayout(self.cell_hbox2)
        self.cell_vbox.addLayout(self.cell_hbox3)
        self.cell_vbox.addStretch(1)
        self.group.setLayout(self.cell_vbox)
        self.vbox.addWidget(self.group)

    def scan(self):
        self.get_mac_test()
        with open('scan_result.txt', 'r') as f:
            scan_result = f.read()
            #print(scan_result)

        if scan_result[:100].find('SSID') == -1:
                if scan_result[:100].find('Not Ready') == -1:
                    self.no_pon = QLabel('Wi-Fi сканер недоступен.')
                    self.clear_vbox()
                    self.vbox.addWidget(self.no_pon)
                    self.vbox.addStretch(1)
                    self.aps = []
        else:
            self.get_mac_test()
            self.clear_vbox()
            cells = scan_result.split('SSID: "')
            cells.remove(cells[0])  # удаляет все до первой SSID
            self.aps = []
            for i in range(len(cells)):
                one = cells[i].split('\n')
                self.aps.append({})
                self.aps[i]['ESSID'] = one[0].strip('"')
                if self.aps[i]['ESSID'] == '' or self.aps[i]['ESSID'] == '"' or self.aps[i]['ESSID'].find('x00') != -1:
                    self.aps[i]['ESSID'] = '<hidden>'
                try:
                    self.aps[i]['MAC'] = one[2].split(' ')[1]
                except:
                    self.aps[i]['MAC'] = ' '
                try:
                    if one[1].find('Channel:') == 64:
                        self.aps[i]['Channel'] = one[1].split(':')[5].strip(' ')
                    if one[1].find('Channel:') == 80:
                        self.aps[i]['Channel'] = one[1].split(':')[6].strip(' ')
                except:
                    self.aps[i]['Channel'] = ' '
                try:
                    self.aps[i]['Sequrity'] = one[7].split(':')[1].strip(' ') + '/' + one[6].split(':')[1].strip(' ')
                    if one[7].split(':')[1].strip(' ') == '':
                        self.aps[i]['Sequrity'] = ''
                except:
                    self.aps[i]['Sequrity'] = ''
                try:
                    self.aps[i]['Power'] = one[1].split(':')[2].strip(' ')[:9].strip(' ')
                except:
                    self.aps[i]['Power'] = ' '
                self.aps[i]['Frequency'] = ' '
                for k in range(len(one)):
                    if one[k].find('0MHz') != -1:
                        self.aps[i]['Frequency'] = one[k].strip(' ').split(' ')[4]
            self.sort_cells()
            for i in self.sorted_aps:
                self.add_lay(i)
            self.vbox.addStretch(1)


    def sort_cells(self):
        self.sorted_aps = sorted(self.aps, key=itemgetter('Power')) # сортирует элементы списка словарей по параметру словарей (по можности сигнала)
        for i in range(len(self.sorted_aps)):
            if self.test_mac:
                if self.sorted_aps[i]['MAC'].upper()[:-2] == self.test_mac.upper()[:-2] and self.response != None:
                    self.test_essid = self.sorted_aps[i]['ESSID']
                    self.sorted_aps.insert(0, self.sorted_aps.pop(i))

    def clear_vbox(self):
        for cnt in reversed(range(self.vbox.count())):
            widget = self.vbox.takeAt(cnt).widget()
            if widget is not None:
                widget.deleteLater()

    def get_mac_test(self):
            with open('config.txt', 'r') as conf:
                conf_text = conf.read()
                self.new_ip = conf_text.split('\n')[1].split('=')[1]
            arp = os.popen("cat /proc/net/arp").read()
            arp = arp.strip('\n').split('\n')
            for i in range(len(arp)):
                arp[i] = arp[i].split(' ')
                arp[i] = [x for x in arp[i] if x]
                if arp[i][0] == self.new_ip:
                    self.test_mac = arp[i][3]
                    self.response = 1
                    break
                else:
                    self.test_mac = None
            if self.test_mac == None:
                try:
                    self.response = subprocess.check_output(
                        ['ping', '-c', '2', '-W', '1', '-i', '0.2', self.new_ip],
                        stderr=subprocess.STDOUT,  # get all output
                        universal_newlines=True  # return string not bytes
                    )
                except subprocess.CalledProcessError:
                    self.response = None

    def show_settings(self):
        self.sett = Settings()
        self.sett.setWindowModality(Qt.ApplicationModal)
        self.sett.show()

class Settings(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 200, 300, 150)
        self.setWindowTitle('Настройки')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.init_settings()

    def init_settings(self):
        self.lay_v = QVBoxLayout()
        self.lay_v_h1 = QHBoxLayout()
        self.lay_v_h2 = QHBoxLayout()
        self.lay_v_h3 = QHBoxLayout()
        with open('config.txt', 'r') as conf:
            conf_text = conf.read()
            self.telnet_ip = conf_text.split('\n')[0].split('=')[1]
            self.cpe_ip = conf_text.split('\n')[1].split('=')[1]

        self.telnet_ip_label = QLabel('IP адрес сканера: ')
        self.telnet_ip_input = QLineEdit(text=self.telnet_ip)
        self.cpe_ip_label = QLabel('IP адрес CPE: ')
        self.cpe_ip_input = QLineEdit(text=self.cpe_ip)
        self.ok_button = QPushButton("Принять")
        self.ok_button.clicked.connect(self.confirm_settings)
        self.cancel_button = QPushButton('Отменить')
        self.cancel_button.clicked.connect(self.cancel_settings)

        self.lay_v_h1.addWidget(self.telnet_ip_label)
        self.lay_v_h1.addStretch(1)
        self.lay_v_h1.addWidget(self.telnet_ip_input)

        self.lay_v_h2.addWidget(self.cpe_ip_label)
        self.lay_v_h2.addStretch(1)
        self.lay_v_h2.addWidget(self.cpe_ip_input)

        self.lay_v_h3.addStretch(1)
        self.lay_v_h3.addWidget(self.ok_button)
        self.lay_v_h3.addWidget(self.cancel_button)
        self.lay_v_h3.addStretch(1)

        self.lay_v.addStretch(1)
        self.lay_v.addLayout(self.lay_v_h1)
        self.lay_v.addLayout(self.lay_v_h2)
        self.lay_v.addStretch(1)
        self.lay_v.addLayout(self.lay_v_h3)

        self.setLayout(self.lay_v)

    def cancel_settings(self):
        self.close()

    def confirm_settings(self):
        self.telnet_ip = self.telnet_ip_input.text()
        self.cpe_ip = self.cpe_ip_input.text()

        with open("config.txt", 'w') as conf:
            conf.write('scanner_ip=' + self.telnet_ip + '\ncpe_ip=' + self.cpe_ip)

        self.close()








if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.timer.start()

    sys.exit(app.exec_())
