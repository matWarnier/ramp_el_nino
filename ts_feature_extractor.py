import numpy as np
from scipy import signal



en_lat_bottom = -5
en_lat_top = 5
en_lon_left = 360 - 170
en_lon_right = 360 - 120

en_f_lat_bottom = -10
en_f_lat_top = 10
en_f_lon_left = 160
en_f_lon_right = 270    

def get_enso_mean(tas):
    return tas.loc[:, en_lat_bottom:en_lat_top, en_lon_left:en_lon_right].mean(dim=('lat','lon'))


def select_box(tas):
    return tas.loc[:, en_f_lat_bottom:en_f_lat_top, en_f_lon_left:en_f_lon_right]

def reshape_tas(tas):
    #
    # Get n_time , n_long , n_lat
    theShape = tas.shape
    n_time,n_lat,n_long = theShape[0],theShape[1],theShape[2]            
    print n_time,n_lat,n_long

    return tas.values.reshape(-1,12,n_lat,n_long)


#return tas.loc[:, en_f_lat_bottom:en_f_lat_top, en_f_lon_left:en_f_lon_right]

#apply reshape

#reshaped_tas = reshape_tas(selected_tas)

#plt.plot(reshaped_xray['tas'][1:36,30,37])

#plt.plot(selected_tas[1:360,30,11])
#plt.plot(reshaped_tas[1:10,:,-1,11].ravel())

#print reshaped_tas.shape

class FeatureExtractor(object):

    def __init__(self):
        pass

    def fit(self, temperatures_xray, n_burn_in, n_lookahead):
        pass

    def transform(self, resampled_xray, n_burn_in, n_lookahead, skf_is):
        """Use world temps as features."""        
        # Set all temps on world map as features
        #valid_range = range(n_burn_in, temperatures_xray['time'].shape[0] - n_lookahead)
        #time_steps, lats, lons = temperatures_xray['tas'].values.shape
        #X = temperatures_xray['tas'].values.reshape((time_steps,lats*lons))
        #X = X[valid_range,:]

        tas = select_box(resampled_xray['tas']) 

        valid_range = range(n_burn_in, resampled_xray['time'].shape[0] - n_lookahead)
        #enso = get_enso_mean(temperatures_xray['tas'])
        # reshape the vector into a table years as rows, months as columns
        #enso_matrix = enso.values.reshape((-1,12))

        theShape = tas.shape
        n_time,n_lat,n_long = theShape[0],theShape[1],theShape[2]            
        #print n_time,n_lat,n_long   
        enso_matrix = tas.values.reshape(-1,12,n_lat,n_long)

        count_matrix = np.ones(enso_matrix.shape)
        # compute cumulative means of columns (remember that you can only use
        # the past at each time point) and reshape it into a vector
        enso_monthly_mean = (enso_matrix.cumsum(axis=0) / count_matrix.cumsum(axis=0)).reshape(-1,n_lat,n_long)#.ravel()
        # roll it backwards (6 months) so it corresponds to the month of the target

        enso_anomaly = tas - enso_monthly_mean

        enso_anomaly_rolled = np.roll(enso_anomaly, n_lookahead - 12,axis = 0)
        # select valid range
        enso_anomaly_rolled_valid = enso_anomaly_rolled[valid_range,:,:]
        # reshape it into a matrix of a single column
        X = enso_anomaly_rolled_valid.reshape(-1,n_lat*n_long)

        return X

  
