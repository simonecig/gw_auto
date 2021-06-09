import numpy as np
import matplotlib.pyplot as plt
import os
from shutil import copy
from tabulate import tabulate

def main():

    '''os.chdir('/home/ciga/builds/qe-easy/bin/')'''
    
    nameeasy=input('Name of output easy file: \n')
    if(nameeasy==''):
        nameeasy='si_easy.out13'
    prefix=input('Prefix: \n')
    if(prefix==''):
        prefix='si64atoms'
    imin=input('KS state min:\n')
    if(imin==''):
        imin='128'
    imin=int(imin)
    imax=input('KS state max:\n')
    if(imax==''):
        imax='129'
    imax=int(imax)
    irange=imax-imin+1
    smin=input('spin min:\n')
    if(smin==''):
        smin='1'
    smin=int(smin)
    smax=input('spin max:\n')
    if(smax==''):
        smax='1'
    smax=int(smax)
    srange=smax-smin+1
    srange=2

    lfile=input('New file convention t/f:  \n')
    lfile=bool(lfile=='t' or lfile=='T')             

    imode=input('Kind of Importance sampling: 0-None  1-|Psi>  2-Vc|Psi> ?\n')
    imode=int(imode)
  
    """Find out points which have been acuatlly calculated"""
    f = open(nameeasy,mode='r')
    line_prev='none'
    coor=[]
    wavefunction=[]
    wavefunction.append([])
    wavefunction.append([])
    vcfunction=[]
    vcfunction.append([])
    vcfunction.append([])
    vcinte=[]
    vcinte.append([])
    vcinte.append([])   
    
    for i in range(3):
        coor.append([])

   
    while(True):
        line=f.readline()
        if not line :
                break;
        wordlist=line.split()
        for i in range (len(wordlist)):
            if(wordlist[i]=='PASSED'):
                if(wordlist[i+1]=='1'):
                    wordlist_prev=line_prev.split()
                    wavefunction[0].append([])
                    wavefunction[1].append([])
                    vcfunction[0].append([])
                    vcfunction[1].append([])
                    vcinte[0].append([])
                    vcinte[1].append([])
                    for j in range(3):
                        coor[j].append(wordlist_prev[j+1])
                    ifound=0
                    while(True):
                        line=f.readline()                        
                        if not line :
                            print('Tiro via \n')
                            for j in range(3):
                                coor[j].pop()
                            wavefunction[0].pop()
                            wavefunction[1].pop()
                            vcfunction[0].pop()
                            vcfunction[1].pop()
                            vcinte[0].pop()
                            vcinte[1].pop()
                            break;
                        wordlist=line.split()
                        if(len(wordlist)>0):
                            if(wordlist[0]=='WAVE_FUNCTIONS' and (int(wordlist[4]) in  range(imin,imax+1))):
                                 ifound+=1
                                 if(ifound<=(imax-imin+1)):
                                       wavefunction[smin-1][-1].append(float(wordlist[5]))
                                       vcinte[smin-1][-1].append(float(wordlist[6]))
                                       vcfunction[smin-1][-1].append(float(wordlist[7]))
                                 elif(smax-smin>0 and ifound<=(imax-imin+1)*2):                                  
                                       wavefunction[smin][-1].append(float(wordlist[5]))
                                       vcinte[smin][-1].append(float(wordlist[6])) 
                                       vcfunction[smin][-1].append(float(wordlist[7])) 
                                 else:
                                     break
                                 if(ifound==(imax-imin+1)*(smax-smin+1)):
                                     break
                            elif(wordlist[0]=='COORDINATES:'):
                                 for j in range(3):
                                    coor[j].pop()
                                 wavefunction[0].pop()
                                 wavefunction[1].pop()
                                 vcfunction[0].pop()
                                 vcfunction[1].pop()
                                 vcinte[0].pop()
                                 vcinte[1].pop()
                                 break
        line_prev=line+' '
    f.close()
    npoints=len(coor[0])           
    print('Found points : '+str(npoints)+'\n')

    '''detrmine how may frequency points'''
    coorf=[]
    for ip in range(3):
        if(int(coor[ip][0])< 10):
            coorf.append('000'+coor[ip][0])
        elif(int(coor[ip][0])< 100):
            coorf.append('00'+coor[ip][0])
        elif(int(coor[ip][0])< 1000):
            coorf.append('0'+coor[ip][0])
        else:
            coorf.append(coor[ip][0])

    if(imin<10):
        label='0000'+str(imin)
    elif(imin<100):
        label='000'+str(imin)
    elif(imin<1000):
        label='00'+str(imin)
    elif(imin<10000):
        label='0'+str(imin)
    else:
        label=str(imin)

    if(imin<10):
        label0='000'+str(imin)
    elif(imin<100):
        label0='00'+str(imin)
    elif(imin<1000):
        label0='0'+str(imin)
    else:
        label0=str(imin)
        
    if(lfile):    
      if(smin==2):
          f=open(prefix+'-gwl_orbital_1_'+label0+'/im_on_im_r_'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
      else:
          f=open(prefix+'-gwl_orbital_1_'+label0+'/im_on_im_r_'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
    else:
      if(smin==2):
          f=open(prefix+'-im_on_im_r_'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
      else:
          f=open(prefix+'-im_on_im_r_'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
    nfreq=0
    freqs=[]
    while(True):
        line=f.readline()
        if not line :               
            break;
        wordlist=line.split()
        freqs.append(float(wordlist[0]))
        nfreq+=1
            
    f.close()


    sigma=np.zeros((nfreq,npoints,irange,srange),'complex64')
    for i in range(npoints):
        '''print(str(i+1)+ ' ' +str(coor[0][i])+ ' '+  str(coor[1][i])+ ' ' +str(coor[2][i])+ '\n')'''

        coorf=[]
        for ip in range(3):
           if(int(coor[ip][i])< 10):
               coorf.append('000'+coor[ip][i])
           elif(int(coor[ip][i])< 100):
               coorf.append('00'+coor[ip][i])
           elif(int(coor[ip][i])< 1000):
               coorf.append('0'+coor[ip][i])
           else:
               coorf.append(coor[ip][i])
        

        
        for iss in range(smin-1,smax):
            for ivv in range(imin,imax+1):
                '''print('Wave functions value : '+str(iss)+'  '+str(wavefunction[iss][i][ivv-imin])+'\n')'''
                
                if(ivv<10):
                    label='0000'+str(ivv)
                elif(ivv<100):
                    label='000'+str(ivv)
                elif(ivv<1000):
                    label='00'+str(ivv)
                elif(ivv<10000):
                    label='0'+str(ivv)
                else:
                    label=str(ivv)

                if(ivv<10):
                    label0='000'+str(ivv)
                elif(ivv<100):
                    label0='00'+str(ivv)
                elif(ivv<1000):
                    label0='0'+str(ivv)
                else:
                    label0=str(ivv)

                if(lfile):    
                   if(iss==0):
                       f=open(prefix+'-gwl_orbital_1_'+label0+'/im_on_im_r_'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
                   else:
                       f=open(prefix+'-gwl_orbital_2_'+label0+'/im_on_im_r_2'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')

                   if(iss==0):
                       g=open(prefix+'-gwl_orbital_1_'+label0+'/re_on_im_r_'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
                   else:
                       g=open(prefix+'-gwl_orbital_2_'+label0+'/re_on_im_r_2'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
                       
                else:
                  if(iss==0):
                      f=open(prefix+'-im_on_im_r_'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
                  else:
                      f=open(prefix+'-im_on_im_r_2'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')

                  if(iss==0):
                     g=open(prefix+'-re_on_im_r_'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
                  else:
                     g=open(prefix+'-re_on_im_r_2'+coorf[0]+'_'+coorf[1]+'_'+coorf[2]+'__'+label,mode='r')
                     
                for ifreq in range (nfreq):
                    linef=f.readline()
                    if not linef :               
                         break;
                    lineg=g.readline()
                    wordf=linef.split()
                    wordg=lineg.split()
                    sigma[ifreq][i][ivv-imin][iss]=complex(float(wordg[2]),float(wordf[2]))
                    
                f.close()
                g.close()
        
    thrs=input('Thresholds for wavefunctions\n')
    if(thrs==''):
        thrs='0. 0.00001 0.0001 0.001 0.01 0.1'
    wordthrs=thrs.split()
    thrs=[]
    for it in range(len(wordthrs)):
        thrs.append(float(wordthrs[it]))
    nit=len(thrs)

    dist=input('Distances between consecutive points 3d array\n')
    if(dist==''):
        dist='1'
    worddist=dist.split()
    dist=[]
    for idd in range(len(worddist)):
        dist.append(int(worddist[idd]))
    ndist=len(dist)
            
   
    sigmaout=np.zeros((nfreq,irange,srange,nit,ndist),'complex64')
    npoints_used=np.zeros((irange,srange,nit,ndist),'int64')
    norm_used=np.zeros((irange,srange,nit,ndist),'float64')
    
    for idd in range(ndist):
        for it in range(nit):
            for iss in range(smin-1,smax):
                for ivv in range(imin,imax+1):
                    norm=0.
                    inorm=0
                    for i in range(npoints):
                      r1=int(coor[0][i])
                      r2=int(coor[1][i])
                      r3=int(coor[2][i])
                      if((r1-1)%dist[idd] == 0 and (r2-1)%dist[idd] == 0 and  (r3-1)%dist[idd] == 0 ):
                        if(abs(wavefunction[iss][i][ivv-imin])>thrs[it]):
                             '''print('Using point: '+coor[0][i]+' '+coor[1][i]+' '+coor[2][i]+'\n')'''
                             if(imode==1):
                                norm+=(wavefunction[iss][i][ivv-imin])**2.
                                fact=wavefunction[iss][i][ivv-imin]
                             elif(imode==0):
                                norm+=1
                                fact=wavefunction[iss][i][ivv-imin]
                             elif(imode==2):
                                norm+=(wavefunction[iss][i][ivv-imin])*(vcfunction[iss][i][ivv-imin])/(vcinte[iss][i][ivv-imin])
                                fact=wavefunction[iss][i][ivv-imin]
                             inorm+=1
                             for ifreq in range (nfreq):
                                  sigmaout[ifreq,ivv-imin,iss,it,idd]+=sigma[ifreq,i,ivv-imin,iss]*fact
                    npoints_used[ivv-imin,iss,it,idd]=inorm
                    norm_used[ivv-imin,iss,it,idd]=norm
                    '''print('Wavefunction: '+str(ivv)+' '+str(iss)+' Points: '+str(inorm)+' Norm: '+str(norm)+'\n')'''
                    if(norm>0.):
                        for ifreq in range (nfreq):
                            sigmaout[ifreq,ivv-imin,iss,it,idd]/=norm
                    else:
                        for ifreq in range (nfreq):
                            sigmaout[ifreq,ivv-imin,iss,it,idd]=0.


    
    x=np.ones(nfreq)
    for ifreq in range(nfreq):
        x[ifreq]=freqs[ifreq]
    colors=('b','g','r','c','m','y','k')
    query=input('Make graphs?\n')
    if(query==''):
        query='Y'
    if(query=='Y' or query == 'y'):
     
        for iss in range(smin-1,smax):
            for ivv in range(imin,imax+1):
              ic=0
              for idd in range(ndist): 
                 for it in range(nit):
                   sr=np.ones(nfreq)
                   sim=np.ones(nfreq)
                   for ifreq in range(nfreq):
                      sr[ifreq]=sigmaout[ifreq,ivv-imin,iss,it,idd].real
                      sim[ifreq]=sigmaout[ifreq,ivv-imin,iss,it,idd].imag
           
                   plt.plot(x,sr,colors[ic]+'-',label='Thrs: '+str(thrs[it])+' Delta grid: '+str(dist[idd])+' N. points: '+str(npoints_used[ivv-imin,iss,it,idd]))
                   plt.plot(x,sim,colors[ic]+'--')
                   ic+=1
              plt.legend()
              plt.show()

             
    try:         
        os.mkdir('./fitdir')
    except OSError as error: 
        print(error) 
    try:
        copy(prefix+'_fit.in','./fitdir/')
    except: 
        print('file already copied\n')     
    try:
        copy(prefix+'-bands.dat','./fitdir/')
    except:
        print('file already copied\n')    
      
        
    os.chdir('./fitdir')
    f=open(prefix+'_fit.in',mode='r')
    g=open('fit.in',mode='w')
    while(True): 
        line=f.readline()
        if not line :
                break;
        wordlist=line.split()
        if(len(wordlist)>0):
           if('i_min' in wordlist[0]):
               g.write('ggwin%i_min='+str(imin)+'\n')
           elif('i_max' in wordlist[0]):
               g.write('ggwin%i_max='+str(imax)+'\n')
           else:
               g.write(line)
        
    f.close()
    g.close()

    energy=np.zeros((4,irange,srange,nit,ndist),'float64')
    imenergy=np.zeros((irange,srange,nit,ndist),'float64')


    for idd in range(ndist):
     for it in range(nit):
        for iss in range(smin-1,smax):
                for ivv in range(imin,imax+1):
                    
                    if(ivv<10):
                        label='0000'+str(ivv)
                    elif(ivv<100):
                        label='000'+str(ivv)
                    elif(ivv<1000):
                        label='00'+str(ivv)
                    elif(ivv<10000):
                        label='0'+str(ivv)
                    else:
                        label=str(ivv)
                        
                    if(iss==0):
                        fr=open(prefix+'-re_on_im'+label,mode='w')
                        fi=open(prefix+'-im_on_im'+label,mode='w')
                    else:
                        fr=open(prefix+'-re_on_im2'+label,mode='w')
                        fi=open(prefix+'-im_on_im2'+label,mode='w')
                    for ifreq in range(nfreq):
                        fr.write(str(x[ifreq])+' 0.0000 '+str(sigmaout[ifreq,ivv-imin,iss,it,idd].real)+ ' 0.0000\n')
                        fi.write(str(x[ifreq])+' 0.0000 '+str(sigmaout[ifreq,ivv-imin,iss,it,idd].imag)+ ' 0.0000\n')

                    fr.close()
                    fi.close()
        os.system('/home/ciga/builds/qe-easy/bin/gww_fit.x < fit.in > fit.out')
        os.system('grep State: fit.out > results.out')
        f=open('results.out',mode='r')
        ivv=0
        iss=0
        while(True): 
            line=f.readline()
            if not line :
                break;
            line=line.replace(':',' ')
            wordlist=line.split()
            if('LDA' in wordlist[1]):
                energy[0,ivv,iss,it,idd]=float(wordlist[2])
                energy[1,ivv,iss,it,idd]=float(wordlist[4])
                energy[2,ivv,iss,it,idd]=float(wordlist[6])
                energy[3,ivv,iss,it,idd]=float(wordlist[8])
                ivv+=1
            elif(wordlist[2]=='GW'):
                if(ivv==irange):
                    ivv=0
                imenergy[ivv,iss,it,idd]=float(wordlist[4])
                ivv+=1
                if(ivv==irange):
                    ivv=0
                    iss+=1
            
            
        f.close()
    t1=np.zeros((irange*2,nit*ndist+1),'float64')
    tt=[]
    for ivv in range(irange):
      tt.append([])
      tt.append([])
      tt[ivv*2].append(ivv+imin)
      tt[ivv*2+1].append('#')
      for idd in range(ndist):
        for it in range(nit):
            tt[ivv*2].append(energy[2,ivv,smin-1,it,idd])
            tt[ivv*2+1].append(npoints_used[ivv,smin-1,it,idd])

    labels=[]
    labels.append('State: ')
    for idd in range(ndist):
      for it in range(nit):
         labels.append('Thrs: '+wordthrs[it]+' Grid space: '+worddist[idd])

    table = tabulate(tt, labels, tablefmt="fancy_grid",numalign="right")
    print(table)

    if(smax != smin):
        t2=np.zeros((irange,nit*ndist+1),'float64')
        tt=[]  
        for ivv in range(irange):
          tt.append([])
          tt.append([])
          tt[ivv*2].append(ivv+imin)
          tt[ivv*2+1].append('#')
          t2[ivv,0]=ivv
          for idd in range(ndist):
            for it in range(nit):
                tt[ivv*2].append(energy[2,ivv,1,it,idd])
                tt[ivv*2+1].append(npoints_used[ivv,1,it,idd])
                t2[ivv,it+idd*nit+1]=energy[2,ivv,smax-1,it,idd]
        
        table = tabulate(tt, labels, tablefmt="fancy_grid")
        print(table)

    g=open('qpe_range.dat',mode='w')
    g.write(str(smax*(imax-imin+1))+'\n')
    for iss in range(srange):
        for ivv in range(irange):
            g.write(str(ivv)+ ' '+ str(energy[0,ivv,iss,0,0])+' '+str(energy[1,ivv,iss,0,0])+\
                    ' '+str(energy[2,ivv,iss,0,0])+' '+str(energy[1,ivv,iss,0,0])+'\n')
    g.close()


if __name__ == "__main__":
    main()
