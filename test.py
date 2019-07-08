
import glob																							
import os																						    
import numpy																						
import h5py																							
import librosa																						


path = '/dcase2019_task1_baseline/datasets/TAU-urban-acoustic-scenes-2019-development/audio/';		
mount_path = '/var/mount_directory/'																
files = [];																							




def Get_FileName():
	global files;																					
	os.chdir(path);																					
	files= glob.glob('*.wav');																		
	numpy.save(mount_path + 'filename', files);														




def FFT_FileSave():
	h5file = h5py.File(mount_path + 'data_File', 'x');												
	h5file.create_group('data_folder');																
	for filename in files:																			
		data, fs = librosa.load(path + filename, sr=48000, offset=0.0, duration=10.0);				
		spectrum = numpy.abs(librosa.stft(data));													
		h5file.create_dataset('data_folder/' + filename, data= spectrum);							
		h5file.flush();																				
	h5file.flush();																					
	h5file.close();																					




def Load_FileData():
	global files;																					
	files = numpy.load(mount_path + 'filename.npy');												




def main():
	Get_FileName();																					
	FFT_FileSave();																					
	Load_FileData();																				




if __name__ == '__main__':																			
	main();																							





	# http://blog.brainpad.co.jp/entry/2018/04/17/143000   FFT
	# https://qiita.com/aoksh/items/cd124183f38e19def731   HDF5