# -*- coding: utf-8 -*-
#系统库
import  sys
import os
import time
import datetime
#第三方库
from pathlib import Path
import  requests
from bs4 import BeautifulSoup

class MovieDownMod(object):
    def __init__(self):
        self.parseEntry = "http://jx.618g.com/?url="
        self.movieEditStr = ""
        self.movieLocalEditStr = "" #"E:\code_workpath\python\movie\mp4"暂时定义无效
        self.outputFile = 'new.mp4'
        self.timeCount = 0
        self.__InitPathPathRoot__()
        self.__InitFfmpegPath__()

    def __InitPathPathRoot__(self):
        self.appPath =  str(sys.argv[0])
        self.pathRoot = str(Path(self.appPath).parent)
        print("run this app froom path:\n" + self.appPath)
    def __InitFfmpegPath__(self):
        if 'exe' in self.pathRoot:
            self.ffmpegExe = Path(str(self.pathRoot)).parent + r'\ffmpeg.exe'
        else:
            self.ffmpegExe = r'D:\install_package\ffmpeg-20200623-ce297b4-win64-static' \
                        r'\ffmpeg-20200623-ce297b4-win64-static\bin\ffmpeg.exe'
        print('ffmpeg path:\n' + self.ffmpegExe)
        if not Path(self.ffmpegExe).is_file():
            print('error:ffmpeg is not install or not in the package')
            time.sleep(5)
            return None

    def __CreateMovieLocalPath__(self, objWin):
        if self.movieLocalEditStr is " ":
            objWin.printfText("error:movieLocalEditStr inpit inaild")
            return None
        else:
            path = Path(self.movieLocalEditStr)
            if path.is_dir():
                pass
            else:
                path.mkdir(parents=True, exist_ok=True)
            self.pathText = self.movieLocalEditStr + r'\debug'
            Path(self.pathText).mkdir(parents=True, exist_ok=True)
            objWin.printfText("movie will save to: " + self.movieLocalEditStr)
            objWin.printfText("html file will save to: " + self.pathText)
    def __GetM3U8TextFromHtml__(self, objWin):
        if self.movieEditStr is "":
            objWin.printfText('error:url of movie is not valid')
            return None
        #创建一个空文件
        m3u8UrlTextFile = self.pathText + r'\m3u8UrlTextFile.bin'
        if Path(m3u8UrlTextFile).is_file():
            pass
        else:
            with open(m3u8UrlTextFile, 'a') as file:
                file.close()
        #sys._getframe().f_code.co_name可以打印当前函数名
        objWin.printfText("m3u8UrlTextFile is: " + m3u8UrlTextFile)
        #request请求并写进文件
        m3u8url = "" + self.parseEntry + self.movieEditStr
        text = requests.get(m3u8url).text
        with open(m3u8UrlTextFile, 'w') as file:
            file.write(text)
            objWin.printfText(Path(m3u8UrlTextFile).name + "save success")
        return text
    def __ParseM3U8Http__(self, text, objWin):
        soup = BeautifulSoup(text, "html.parser")
        objWin.printfText(str(soup.prettify()))
        iframs = soup.find_all('iframe')
        for ifram in iframs:
            if 'm3u8' in ifram.attrs['src']:
                objWin.printfText(ifram.attrs['src'])
                m3u8UrlHttpIndex = str(ifram.attrs['src']).find('http')
                m3u8urlHttp = ifram.attrs['src'][m3u8UrlHttpIndex:]
                objWin.printfText("m3u8httpAddr is parsed success: " + m3u8urlHttp)
            else:
                objWin.printfText("error:m3u8httpAddr is parse fail")
                print("error:m3u8httpAddr is parse fail")
        return m3u8urlHttp
    def __CreateDownLoadCmd__(self, text, objWin):
        m3u8urlHttp = self.__ParseM3U8Http__(text, objWin)
        print('m3u8 http url is: ' + m3u8urlHttp)
        objWin.printfText('m3u8 http url is: ' + m3u8urlHttp)
        cmd = self.ffmpegExe + ' -i ' + m3u8urlHttp + ' -vcodec copy -acodec copy ' + self.movieLocalEditStr + '\\' + self.outputFile
        return cmd
    def __DownLoadByFfmpeg__(self, cmd, objWin):
        objWin.printfText(time.ctime())
        timeStart = datetime.datetime.now()
        ret = os.system(cmd)
        timeEnd = datetime.datetime.now()
        objWin.printfText(time.ctime())
        objWin.printfText('load finish ret ' + str(ret) + ', ' + \
                          'resume time ' + str(timeEnd - timeStart) + 'sec')
        self.timeCount += 1
        return ret


    def __DownLoadByM3U8Url__(self, objWin):
        objWin.printfText(">>>>>>>>>>>>>>MovieDownMod is processing<<<<<<<<<")
        #1.创建电影保存的本地地址
        self.__CreateMovieLocalPath__(objWin)
        #2.通过jx168获取含有名m3u8地址的网页以供解析
        text = self.__GetM3U8TextFromHtml__(objWin)
        objWin.printfText('ffmpeg path is: ' + self.ffmpegExe)
        #3.构建下载命令ffmpeg -i xxx,其中
        cmd = self.__CreateDownLoadCmd__(text, objWin)
        print('will excute cmd is : ' + cmd)
        objWin.printfText('will excute cmd is : ' + cmd)
        self.__DownLoadByFfmpeg__(cmd, objWin)

    # objWin是外面传进来的对象
    def SetMovieEditStr(self, input, objWin):
        self.movieEditStr = "" + input
        objWin.printfText('movieEditStr is: ' + self.movieEditStr)
    def GetMovieEditStr(self):
        return self.movieEditStr
    def SetMovieLocalEditStr(self, input, objWin):
        self.movieLocalEditStr = "" + input
        objWin.printfText('movieLocalEditStr is: ' + self.movieLocalEditStr)
    def GetMovieLocalEditStr(self):
        return self.movieLocalEditStr
    def DownLoadPro(self, cmd, objWin):
        if cmd == 1:
            self.__DownLoadByM3U8Url__(objWin)
        elif cmd == 0:
            objWin.printfText("MovieDownMod is canceling, no support now")
