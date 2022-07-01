import time

t1 = time.time()
last_error = 0
d = 0
integral = 0
patch = 0
moving_avarege = [0]*20

def control(left_sensor, right_sensor, speed):
    
    global t1, last_error, moving_avarege, d, patch, integral
    
    def PD(error, last_error, integral, dt, KP=0.24,KD=0.01):
        
        # P
        P = KP*error
        
        # D
        D = KD*(error-last_error)/dt
    
        # Sum the individuals corrections
            
        return P, D
   
    def get_curve(moving_avarege):
        
        threshold = 0.3
        
        return abs(sum(moving_avarege)/len(moving_avarege)) > threshold
    
    def get_patch(curve, d, patch):
        after_curve_distance = 50
        
        if curve:
            return 1, 0
        if patch == 1:
            return 2, d
        if patch == 2 and d >= after_curve_distance:
            return 3, d
        return patch, d
        
    def get_torque(patch, speed):
        speed_limit = 120
        
        if patch == 0:
            return 4000, 0
        if patch == 1:
            if speed > speed_limit:
                return 200, 300
            return 4500, 0
        if patch == 2:
            return 5000, 0
        if patch == 3:
            return 0, 1000
        
        
    # calculate error and time delta
    t2 = time.time()
    dt = t2-t1
    
    error =  right_sensor-left_sensor-0;2
    moving_avarege = moving_avarege[1:]+[error,]
    
    P, D = PD(error, last_error, d, dt)
    correction = P+D
    curve = get_curve(moving_avarege)    
    patch, d = get_patch(curve, d, patch)
    etorque, btorque = get_torque(patch, speed)
    
    t1 = t2
    d += dt*speed
    integral += dt*speed
    last_error = error
        
    out = {
        'engineTorque': etorque,
        'brakingTorque': btorque,
        'steeringAngle': correction,
        'log': [
            { 'name': '0', 'value': 0, 'min':-1, 'max': 1 },
            { 'name': 'patch', 'value': patch, 'min':0, 'max':3},
            { 'name': 'speed', 'value': speed, 'min':0, 'max':200},
            { 'name': 'd', 'value': d, 'min':0, 'max':1000},
            { 'name': 'P', 'value': P, 'min':-1, 'max':1},
            { 'name': 'D', 'value': D, 'min':-1, 'max':1},
            { 'name': 'error', 'value': error, 'min':-2, 'max':2}
                ]
    }
    return out


