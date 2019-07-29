
import glob																							
import os																						    
import numpy																						
import h5py																							
import librosa																						
import matplotlib.pyplot																			
import librosa.display																				


path = '/dcase2019_task1_baseline/datasets/TAU-urban-acoustic-scenes-2019-development/audio/';		
mount_path = '/var/mount_directory/'																
files = ['airport-barcelona-0-0-a.wav']#,'airport-barcelona-0-1-a.wav','airport-barcelona-0-10-a.wav'];																							




def Get_FileName():
	global files;																					
	os.chdir(path);																					
	files= glob.glob('*.wav');																		
	numpy.save(mount_path + 'filename', files);														




def Load_FileData():
	global files;																					
	files = numpy.load(mount_path + 'filename.npy');												




def FFT_FileSave():
	h5file = h5py.File(mount_path + 'data_File', 'x');												
	h5file.create_group('original_data');															
	h5file.create_group('spectrum_data');															
	
	for filename in files:																			
		data, fs = librosa.load(path + filename, sr=48000, offset=0.0, duration=10.0);				
		h5file.create_dataset('original_data/' + filename, data = data);									
		h5file.flush();																				
		
		spectrum = numpy.abs(librosa.stft(data));													
		h5file.create_dataset('spectrum_data/' + filename, data = spectrum);								
		h5file.flush();																				

	h5file.flush();																					
	h5file.close();																					




def Plot_DATA(data, filename):
	h5file = h5py.File(mount_path + 'data_File', 'w');												
	h5file.create_group('plot_DATA');																
	matplotlib.pyplot.figure(figsize=(14,5));														
	matplotlib.pyplot.title('時間波形' + filename);													
	librosa.display.waveplot(data, sr=48000);														
	matplotlib.pyplot.savefig(mount_path + filename + '_data.png' ,dpi=200)							
	h5file.flush();																					
	h5file.close();	
	print('OK_時間')																				




def Plot_spectrogram(spectrum, filename):
	h5file = h5py.File(mount_path + 'data_File', 'w');												
	h5file.create_group('plot_SPE');																
	spe_db = librosa.amplitude_to_db(abs(spectrum));												
	matplotlib.pyplot.figure(figsize=(14,5));														
	matplotlib.pyplot.title('スペクトログラム' + filename);											
	librosa.display.specshow(spe_db, sr=48000, x_axis ='[s]', y_axis='[Hz]');						
	matplotlib.pyplot.colorbar();																	
	matplotlib.pyplot.savefig(mount_path + filename + '_spe.png' ,dpi=200)							
	h5file.flush();																					
	h5file.close();	
	print('OK_SPE')




def Call_PLOT():
	for filename in files:																			
		h5file = h5py.File(mount_path + 'data_File', 'r');											

		data = h5file['original_data/'+ filename][()]											
		h5file.flush();																				
	
		spectrum = h5file['spectrum_data/'+ filename][()]									
		h5file.flush();																				
		h5file.close();																				
		
		Plot_DATA(data, filename);																	
	#	Plot_spectrogram(spectrum, filename);																																				




def main():
	value = 0;																						

	#if value == 0:																					
	#	Get_FileName();																				
	#else:																							
	#	Load_FileData();																			
	
	FFT_FileSave();																					
	Call_PLOT();																					




if __name__ == '__main__':																			
	main();																							





	# http://blog.brainpad.co.jp/entry/2018/04/17/143000   FFT
	# https://qiita.com/aoksh/items/cd124183f38e19def731   HDF5
	# http://villageofsound.hatenadiary.jp/entry/2014/11/12/132121