"""
Fall Detection System — Core Module
Converted from Google Colab notebook to VS Code compatible script.
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

FEATURE_COLS = [
    'accel_x', 'accel_y', 'accel_z',
    'gyro_x',  'gyro_y',  'gyro_z',
    'acc_magnitude', 'gyro_magnitude',
    'mean_acceleration', 'std_acceleration',
    'variance_acceleration', 'signal_magnitude_area',
    'tilt_angle_x', 'tilt_angle_y'
]


def generate_dataset(n=10000):
    np.random.seed(42)
    rows = []
    for _ in range(n):
        activity = np.random.choice(['Sitting','Standing','Walking'], p=[0.30,0.35,0.35])

        if activity == 'Sitting':
            ax=np.random.normal(0.0,0.05); ay=np.random.normal(0.0,0.05); az=np.random.normal(9.80,0.08)
            gx=np.random.normal(0,0.2); gy=np.random.normal(0,0.2); gz=np.random.normal(0,0.2)
            stability,risk,fall_type,fall_detected='Stable','LOW','No Fall',0

        elif activity == 'Standing':
            state=np.random.choice(['stable','unstable','fall'],p=[0.80,0.15,0.05])
            if state=='stable':
                ax=np.random.normal(0.0,0.10); ay=np.random.normal(0.0,0.10); az=np.random.normal(9.80,0.12)
                gx=np.random.normal(0,0.6); gy=np.random.normal(0,0.6); gz=np.random.normal(0,0.3)
                stability,risk,fall_type,fall_detected='Stable','LOW','No Fall',0
            elif state=='unstable':
                ax=np.random.normal(0.0,1.5); ay=np.random.normal(0.0,1.5); az=np.random.normal(9.3,0.4)
                gx=np.random.normal(0,5); gy=np.random.normal(0,5); gz=np.random.normal(0,2.5)
                stability,risk,fall_type,fall_detected='Unstable','HIGH','No Fall',0
            else:
                ft=np.random.choice(['Forward Fall','Backward Fall','Side Fall Right','Side Fall Left'])
                ax=np.random.normal(5.5 if ft=='Forward Fall' else -5.5 if ft=='Backward Fall' else 0.2,0.5)
                ay=np.random.normal(5.5 if ft=='Side Fall Right' else -5.5 if ft=='Side Fall Left' else 0.2,0.5)
                az=np.random.normal(2.5,0.8)
                gx=np.random.normal(0,10); gy=np.random.normal(0,10); gz=np.random.normal(0,7)
                stability,risk,fall_type,fall_detected='Unstable','CRITICAL',ft,1

        else:
            state=np.random.choice(['stable','irregular','fall'],p=[0.82,0.13,0.05])
            if state=='stable':
                ax=np.random.normal(0.5,0.35); ay=np.random.normal(0.1,0.25); az=np.random.normal(9.5,0.35)
                gx=np.random.normal(0,3.5); gy=np.random.normal(0,3.5); gz=np.random.normal(0,2.0)
                stability,risk,fall_type,fall_detected='Stable','LOW','No Fall',0
            elif state=='irregular':
                ax=np.random.normal(0.5,2.0); ay=np.random.normal(0.1,2.0); az=np.random.normal(9.0,0.7)
                gx=np.random.normal(0,6); gy=np.random.normal(0,6); gz=np.random.normal(0,4)
                stability,risk,fall_type,fall_detected='Unstable','MEDIUM','No Fall',0
            else:
                ft=np.random.choice(['Forward Fall','Backward Fall','Side Fall Right','Side Fall Left'])
                ax=np.random.normal(6.0 if ft=='Forward Fall' else -6.0 if ft=='Backward Fall' else 0.2,0.5)
                ay=np.random.normal(6.0 if ft=='Side Fall Right' else -6.0 if ft=='Side Fall Left' else 0.2,0.5)
                az=np.random.normal(2.0,1.0)
                gx=np.random.normal(0,11); gy=np.random.normal(0,11); gz=np.random.normal(0,8)
                stability,risk,fall_type,fall_detected='Unstable','CRITICAL',ft,1

        acc_mag=np.sqrt(ax**2+ay**2+az**2); gyro_mag=np.sqrt(gx**2+gy**2+gz**2)
        sma=(abs(ax)+abs(ay)+abs(az))/3; variance=np.var([ax,ay,az])
        std_acc=np.std([ax,ay,az]); mean_acc=np.mean([ax,ay,az])
        tilt_x=np.degrees(np.arctan2(ax,np.sqrt(ay**2+az**2)))
        tilt_y=np.degrees(np.arctan2(ay,np.sqrt(ax**2+az**2)))

        rows.append({'accel_x':round(ax,4),'accel_y':round(ay,4),'accel_z':round(az,4),
            'gyro_x':round(gx,4),'gyro_y':round(gy,4),'gyro_z':round(gz,4),
            'acc_magnitude':round(acc_mag,4),'gyro_magnitude':round(gyro_mag,4),
            'mean_acceleration':round(mean_acc,4),'std_acceleration':round(std_acc,4),
            'variance_acceleration':round(variance,4),'signal_magnitude_area':round(sma,4),
            'tilt_angle_x':round(tilt_x,4),'tilt_angle_y':round(tilt_y,4),
            'activity':activity,'stability':stability,'risk_level':risk,
            'fall_detected':fall_detected,'fall_type':fall_type})
    return pd.DataFrame(rows)


def train_models(df):
    df = df.dropna().copy()
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[FEATURE_COLS] = scaler.fit_transform(df[FEATURE_COLS])
    X = df_scaled[FEATURE_COLS].copy()

    le_activity=LabelEncoder(); le_fall=LabelEncoder(); le_risk=LabelEncoder()
    y_activity=le_activity.fit_transform(df['activity'])
    y_fall=le_fall.fit_transform(df['fall_type'])
    y_risk=le_risk.fit_transform(df['risk_level'])

    X_train,X_test,y_act_train,y_act_test=train_test_split(X,y_activity,test_size=0.20,random_state=42,stratify=y_activity)
    _,_,y_fall_train,y_fall_test=train_test_split(X,y_fall,test_size=0.20,random_state=42,stratify=y_activity)
    _,_,y_risk_train,y_risk_test=train_test_split(X,y_risk,test_size=0.20,random_state=42,stratify=y_activity)

    ml_models={'Decision Tree':DecisionTreeClassifier(max_depth=15,min_samples_split=5,random_state=42),
               'Random Forest':RandomForestClassifier(n_estimators=200,max_depth=20,random_state=42,n_jobs=-1),
               'KNN':KNeighborsClassifier(n_neighbors=3,metric='euclidean')}
    results={}; trained_models={}
    for name,model in ml_models.items():
        model.fit(X_train,y_act_train)
        y_pred=model.predict(X_test)
        results[name]={'Accuracy':accuracy_score(y_act_test,y_pred),
                       'Precision':precision_score(y_act_test,y_pred,average='weighted'),
                       'Recall':recall_score(y_act_test,y_pred,average='weighted'),
                       'F1-Score':f1_score(y_act_test,y_pred,average='weighted')}
        trained_models[name]=model

    best_model_name=max(results,key=lambda x:results[x]['Accuracy'])
    fall_model=RandomForestClassifier(n_estimators=100,random_state=42,n_jobs=-1)
    fall_model.fit(X_train,y_fall_train)
    risk_model=RandomForestClassifier(n_estimators=100,random_state=42,n_jobs=-1)
    risk_model.fit(X_train,y_risk_train)

    return {'scaler':scaler,'le_activity':le_activity,'le_fall':le_fall,'le_risk':le_risk,
            'best_model':trained_models[best_model_name],'best_model_name':best_model_name,
            'fall_model':fall_model,'risk_model':risk_model,'results':results,
            'X_test':X_test,'y_act_test':y_act_test,'y_fall_test':y_fall_test,'y_risk_test':y_risk_test}


def get_stability(ax,ay,az):
    variance=np.var([ax,ay,az])
    return 'Unstable' if variance>1.5 or abs(ax)>2.0 or abs(ay)>2.0 else 'Stable'


def analyze_sequence(history):
    if len(history)<2: return 'LOW',None
    last=history[-1]; prev=history[-2]
    if last['stability']=='Unstable' and last['activity'] in ['Standing','Walking']:
        if last.get('ax_raw',0)>3.0: return 'CRITICAL','Forward Fall Likely'
        if last.get('ax_raw',0)<-3.0: return 'CRITICAL','Backward Fall Likely'
        if last.get('ay_raw',0)>3.0: return 'CRITICAL','Side Fall Right Likely'
        if last.get('ay_raw',0)<-3.0: return 'CRITICAL','Side Fall Left Likely'
    if prev['activity']=='Walking' and last['activity']=='Standing' and last['stability']=='Unstable':
        return 'HIGH','Instability after stopping from walk'
    if prev['activity']=='Sitting' and last['activity']=='Standing' and last['stability']=='Unstable':
        return 'MEDIUM','Instability when rising from seated position'
    if prev['activity']=='Standing' and last['activity']=='Walking' and last['stability']=='Unstable':
        return 'MEDIUM','Irregular walking pattern detected'
    return 'LOW',None


def generate_explanation(history,risk,prediction):
    if risk=='CRITICAL' and prediction:
        prev_act=history[-2]['activity'] if len(history)>=2 else 'previous activity'
        return f"Fall during {history[-1]['stability'].lower()} {history[-1]['activity'].lower()} after {prev_act.lower()}."
    if risk=='HIGH': return "High risk: sudden stop from walking caused instability."
    if risk=='MEDIUM': return "Moderate risk: abnormal activity transition detected."
    return "Normal activity — no immediate risk detected."


def run_system(raw_sample, history, trained):
    ax=raw_sample['accel_x']; ay=raw_sample['accel_y']; az=raw_sample['accel_z']
    gx=raw_sample['gyro_x'];  gy=raw_sample['gyro_y'];  gz=raw_sample['gyro_z']
    mean_acc=np.mean([ax,ay,az]); std_acc=np.std([ax,ay,az]); var_acc=np.var([ax,ay,az])
    sma=(abs(ax)+abs(ay)+abs(az))/3
    acc_mag=np.sqrt(ax**2+ay**2+az**2); gyro_mag=np.sqrt(gx**2+gy**2+gz**2)
    tilt_x=np.degrees(np.arctan2(ax,az)); tilt_y=np.degrees(np.arctan2(ay,az))
    raw_feat=np.array([[ax,ay,az,gx,gy,gz,acc_mag,gyro_mag,mean_acc,std_acc,var_acc,sma,tilt_x,tilt_y]])
    scaled=trained['scaler'].transform(raw_feat)
    activity=trained['le_activity'].inverse_transform(trained['best_model'].predict(scaled))[0]
    stability=get_stability(ax,ay,az)
    fall_type=trained['le_fall'].inverse_transform(trained['fall_model'].predict(scaled))[0]
    proba=trained['fall_model'].predict_proba(scaled[0].reshape(1,-1))[0]
    confidence=round(max(proba)*100,1)
    history.append({'activity':activity,'stability':stability,'ax_raw':ax,'ay_raw':ay})
    if len(history)>5: history.pop(0)
    risk,prediction=analyze_sequence(history)
    explanation=generate_explanation(history,risk,prediction)
    seq_str=' → '.join([f"{h['activity']}({'U' if h['stability']=='Unstable' else 'S'})" for h in history])
    return {'activity':activity,'stability':stability,'sequence':seq_str,'risk_level':risk,
            'prediction':prediction,'confidence':confidence,'fall_type':fall_type,
            'explanation':explanation,'alert':risk in ['HIGH','CRITICAL']}
