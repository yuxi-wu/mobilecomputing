import pandas as pd
import numpy as np
import json
import peakutils
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import seaborn as sns

def load_json(file):
    '''
    Loads txt file and returns json dict
    '''
    data = {}
    with open(file, encoding='utf-8') as f:
        for line in f:
            d = str(line).replace("'", '"')
            data = json.loads(d)

    return data

def get_sequence(data_list, sensor):
    '''
    Return list of sensor data from data_list
    '''
    l = []
    for i in range(len(data_list)):
        lst = []
        for j in range(len(data_list[i]['seq'])):
            lst.append(data_list[i]['seq'][j]['data'][sensor])
        l.append(lst)

    return l

def get_mean_sd_peaks(seq_data):
    '''
    Calculates the mean, sd, and number of peaks for each sequence of data for each sensor
    '''
    means = []
    stds = []
    peaks = []
    for lst in seq_data:
        means.append(np.mean(lst))
        stds.append(np.std(lst))
        peaks.append(len(peakutils.indexes(lst, thres=0.02/max(lst), min_dist=0.1)))

    return means, stds, peaks

def process_sequence(filename):
    '''
    Loads data and creates dictionary of calculations from accelerometer data
    '''
    data = load_json(filename)

    # obtain actitivy from trace
    activity = data[0]['type']

    # obtain accelerometer data from each axis
    x_accl = get_sequence(data, 'xAccl')
    y_accl = get_sequence(data, 'yAccl')
    z_accl = get_sequence(data, 'zAccl')
    '''
    # obtain gyroscope data from each axis
    x_gyro = get_sequence(data, 'xGyro')
    y_gyro = get_sequence(data, 'yGyro')
    z_gyro = get_sequence(data, 'zGyro')

    # obtain mag sensor data from each axis
    x_mag = get_sequence(data, 'xMag')
    y_mag = get_sequence(data, 'yMag')
    z_mag = get_sequence(data, 'zMag')
    '''

    # calculate means, sd, num peaks for data sequence
    x_accl_mean, x_accl_sd, x_accl_peaks = get_mean_sd_peaks(x_accl)
    y_accl_mean, y_accl_sd, y_accl_peaks = get_mean_sd_peaks(y_accl)
    z_accl_mean, z_accl_sd, z_accl_peaks = get_mean_sd_peaks(z_accl)

    '''
    x_gyro_mean, x_gyro_sd, x_gyro_peaks = get_mean_sd_peaks(x_gyro)
    y_gyro_mean, y_gyro_sd, y_gyro_peaks = get_mean_sd_peaks(y_gyro)
    z_gyro_mean, z_gyro_sd, z_gyro_peaks = get_mean_sd_peaks(z_gyro)

    x_mag_mean, x_mag_sd, x_mag_peaks = get_mean_sd_peaks(x_mag)
    y_mag_mean, y_mag_sd, y_mag_peaks = get_mean_sd_peaks(y_mag)
    z_mag_mean, z_mag_sd, z_mag_peaks = get_mean_sd_peaks(z_mag)
    '''

    clean_data = {
        'activity': [],
        'x_accl_mean': [], 'x_accl_sd': [], 'x_accl_peaks': [],
        'y_accl_mean': [], 'y_accl_sd': [], 'y_accl_peaks': [],
        'z_accl_mean': [], 'z_accl_sd': [], 'z_accl_peaks': []
        # 'x_gyro_mean': [], 'x_gyro_sd': [], 'x_gyro_peaks': [],
        # 'y_gyro_mean': [], 'y_gyro_sd': [], 'y_gyro_peaks': [],
        # 'z_gyro_mean': [], 'z_gyro_sd': [], 'z_gyro_peaks': [],
        # 'x_mag_mean': [], 'x_mag_sd': [], 'x_mag_peaks': [],
        # 'y_mag_mean': [], 'y_mag_sd': [], 'y_mag_peaks': [],
        # 'z_mag_mean': [], 'z_mag_sd': [], 'z_mag_peaks': []
    }

    for i in range(len(x_accl_mean)):
        clean_data['activity'].append(activity)
        clean_data['x_accl_mean'].append(x_accl_mean[i])
        clean_data['x_accl_sd'].append(x_accl_sd[i])
        clean_data['x_accl_peaks'].append(x_accl_peaks[i])
        clean_data['y_accl_mean'].append(y_accl_mean[i])
        clean_data['y_accl_sd'].append(y_accl_sd[i])
        clean_data['y_accl_peaks'].append(y_accl_peaks[i])
        clean_data['z_accl_mean'].append(z_accl_mean[i])
        clean_data['z_accl_sd'].append(z_accl_sd[i])
        clean_data['z_accl_peaks'].append(z_accl_peaks[i])

        '''
        clean_data['x_gyro_mean'].append(x_gyro_mean[i])
        clean_data['x_gyro_sd'].append(x_gyro_sd[i])
        clean_data['x_gyro_peaks'].append(x_gyro_peaks[i])
        clean_data['y_gyro_mean'].append(y_gyro_mean[i])
        clean_data['y_gyro_sd'].append(y_gyro_sd[i])
        clean_data['y_gyro_peaks'].append(y_gyro_peaks[i])
        clean_data['z_gyro_mean'].append(z_gyro_mean[i])
        clean_data['z_gyro_sd'].append(z_gyro_sd[i])
        clean_data['z_gyro_peaks'].append(z_gyro_peaks[i])
        clean_data['x_mag_mean'].append(x_mag_mean[i])
        clean_data['x_mag_sd'].append(x_mag_sd[i])
        clean_data['x_mag_peaks'].append(x_mag_peaks[i])
        clean_data['y_mag_mean'].append(y_mag_mean[i])
        clean_data['y_mag_sd'].append(y_mag_sd[i])
        clean_data['y_mag_peaks'].append(y_mag_peaks[i])
        clean_data['z_mag_mean'].append(z_mag_mean[i])
        clean_data['z_mag_sd'].append(z_mag_sd[i])
        clean_data['z_mag_peaks'].append(z_mag_peaks[i])
        '''

    df = pd.DataFrame(clean_data)
    return df

def process_test_sequence(filename):
    '''
    Loads data and creates dictionary of calculations from accelerometer data
    '''
    data = load_json(filename)

    # obtain actitivy from trace
    activity = data['type']
    
    # obtain accelerometer data from each axis
    x_accl = []
    y_accl = []
    z_accl = []
    time = []
    for seq in data['seq']:
        x_accl.append(seq['data']['xAccl'])
        y_accl.append(seq['data']['yAccl'])
        z_accl.append(seq['data']['zAccl'])
        time.append(seq['time'])

    # calculate means for data sequence
    x_accl_mean = np.mean(x_accl)
    y_accl_mean = np.mean(y_accl)
    z_accl_mean = np.mean(z_accl)
    
    # calculate standard deviations for sequence
    x_accl_sd = np.std(x_accl)
    y_accl_sd = np.std(y_accl)
    z_accl_sd = np.std(z_accl)
    
    # calculate number of peaks for sequence
    x_accl_peaks = len(peakutils.indexes(x_accl, thres=0.02/max(x_accl), min_dist=0.1))
    y_accl_peaks = len(peakutils.indexes(y_accl, thres=0.02/max(y_accl), min_dist=0.1))
    z_accl_peaks = len(peakutils.indexes(z_accl, thres=0.02/max(z_accl), min_dist=0.1))

    clean_data = {
        'activity': activity,
        'x_accl_mean': x_accl_mean, 'x_accl_sd': x_accl_sd, 'x_accl_peaks': x_accl_peaks,
        'y_accl_mean': y_accl_mean, 'y_accl_sd': y_accl_sd, 'y_accl_peaks': y_accl_peaks,
        'z_accl_mean': z_accl_mean, 'z_accl_sd': z_accl_sd, 'z_accl_peaks': z_accl_peaks
    }

    df = pd.DataFrame(clean_data, index=[0])
    return df, time

def plot_traces(plots, activity):
    x,y,z = plots
    plt.figure(figsize=(15,5))
    plt.plot(x, label='x')
    plt.plot(y, label='y')
    plt.plot(z, label='z')
    plt.legend()
    plt.title(activity)
    plt.savefig(activity + '.png')
    plt.show()

def master():
    master = []
    for i in ['driving','standing','walking','jumping']:
        df = process_sequence('class-data/' + i + '.txt')
        master += [df]
    master = pd.concat(master)
    master['activity_factor'] = pd.factorize(master['activity'])[0]
    return master

def splits(df, split_size=0.25):
    y = df['activity_factor']
    X = df.drop(['activity_factor', 'activity'], axis=1)
    return train_test_split(X, y, test_size=split_size, random_state=1234)

def test():
    test = []
    time_list =[]
    for i in ['1','2','3','4']:
        df, time = process_test_sequence('test-data/team9_' + i + '.txt')
        time_list.append(time)
        test += [df]
    test = pd.concat(test)
    test['trace_number'] = ['1','2','3','4']
    test = test.set_index('trace_number')

    return test.drop(['activity'], axis=1), time_list

def calc_speed(df, time_list, trace_num):
	'''
	Given a df and list of time points, calculate average speed using acceleration data
	'''
	time_elapsed = time_list[trace_num][-1] - time_list[trace_num][0]
	x = df.iloc[trace_num]['x_accl_mean']
	y = df.iloc[trace_num]['y_accl_mean']
	z = df.iloc[trace_num]['z_accl_mean']
	a = np.sqrt(x + y + z)

	return a*time_elapsed