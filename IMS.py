import subprocess
import time
import matplotlib.pyplot as plot

encodes = ['libx264','libx265','libvpx-vp9']
bit_rates = ['10','40','80','160','200','350','500','700','900','1000','1500','2000','2500']

fname = input('Please input the video name:')

print('encoding videos')
Coding = []
for encode in encodes:
   for bit_rate in bit_rates:
      start = time.time()
      cmd = './ffmpeg -i '+fname+'.y4m -c:v '+encode+' -b '+ bit_rate +'k '+fname +'_'+bit_rate+'k_' + encode +'.mkv'
      encoding = subprocess.Popen(cmd, shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
      end = time.time()
      duration = end-start
      Coding.append(float(duration))
      encoding.wait()
      print(encode+' '+bit_rate+'kbps '+'finished and complie time (sec):' , (end-start))

print('transforming to yuv')
for encode in encodes:
   for bit_rate in bit_rates:
      cmd = './ffmpeg -i '+fname+'_'+bit_rate+'k_' + encode +'.mkv -s 352x288 '+fname+'_'+bit_rate+'_' + encode +'.yuv'
      encoding = subprocess.Popen(cmd, shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
      encoding.wait()
      print(encode+' '+bit_rate+'kbps '+'finished')

print('calculating PSNR')
PSNR = []
for encode in encodes:
   for bit_rate in bit_rates:
      cmd = './ffmpeg -s 352x288 -i '+fname+'_'+bit_rate+'_' + encode +'.yuv -s 352x288 -i '+fname+'.yuv -lavfi psnr="stats_file=psnr.log" -f null -'
      psnr_c = subprocess.Popen(cmd, shell=True,stderr=subprocess.PIPE)
      psnr_c.wait()
      sout = psnr_c.stderr.readlines()
      index = sout[-1].decode('utf-8').find('e:')
      psnr = sout[-1].decode('utf-8')[index+2:index+11]
      print(encode+' '+bit_rate+'kbps '+'PSNR: '+psnr)
      PSNR.append(float(psnr))

print('calculating SSIM')
SSIM = []
for encode in encodes:
   for bit_rate in bit_rates:
      cmd = './ffmpeg -s 352x288 -i '+fname+'_'+bit_rate+'_' + encode +'.yuv -s 352x288 -i '+fname+'.yuv -lavfi ssim="stats_file=psnr.log" -f null -'
      ssim_c = subprocess.Popen(cmd, shell=True,stderr=subprocess.PIPE)
      ssim_c.wait()
      sout = ssim_c.stderr.readlines()
      index = sout[-1].decode('utf-8').find('l:')
      ssim = sout[-1].decode('utf-8')[index+2:index+9]
      print(encode+' '+bit_rate+'kbps '+'SSIM: '+ssim)
      SSIM.append(float(ssim))


plot.grid(ls='--')
plot.xlabel('bit rate/kbps')
plot.xticks(rotation=45)
plot.ylabel('db')
plot.title('PSNR')
plot.plot(bit_rates,PSNR[0:13], c = 'r',label = 'H.264')
plot.plot(bit_rates,PSNR[13:26],c = 'g',label='H.265')
plot.plot(bit_rates,PSNR[26:39], c = 'b',label='VP9')
plot.legend(loc='upper left')
plot.show()


plot.grid(ls='--')
plot.xlabel('bit rate/kbps')
plot.xticks(rotation=45)
plot.ylabel('SSIM')
plot.title('SSIM')
plot.plot(bit_rates,SSIM[0:13], c = 'r',label = 'H.264')
plot.plot(bit_rates,SSIM[13:26],c = 'g',label='H.265')
plot.plot(bit_rates,SSIM[26:39], c = 'b',label='VP9')
plot.legend(loc='upper left')
plot.show()
 
plot.grid(ls='--')
plot.xlabel('bit rate/kbps')
plot.xticks(rotation=45)
plot.ylabel('Second')
plot.title('Coding time')
plot.plot(bit_rates,Coding[0:13], c = 'r',label = 'H.264')
plot.plot(bit_rates,Coding[13:26],c = 'g',label='H.265')
plot.plot(bit_rates,Coding[26:39], c = 'b',label='VP9')
plot.legend(loc='upper left')
plot.show()
 
