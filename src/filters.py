import cv2 as cv
import numpy as np

def filterFunction(img, filterX = '', value = 0):
    
    # Convirtiendo el valor a entero y definiendo parámetros
    value = np.clip(int(value), -100, 100)
    
    rows,columns,channels=np.shape(img)
    filteredImg = img.copy()
    
    print(rows, columns)
    
    if (filterX == 'brightness'):
        # Se suma el valor a cada canal  de cada pixel en la imagen
        filteredImg = cv.add(img, np.array([float(value)]))
    
    
    elif (filterX == 'contrast'):
        # Se modifica la intensidad de cada canal utilizando el valor medio en RGB (128) 
        # como punto divisorio
        if (value > 0): 
            # valor =   [1, 100]
            # alpha =   [1, 2]
            # beta =    [0, -1]
            value = float(value/100)
            # Se alejan los valores de los canales del punto medio según su intensidad 
            # (0 para los menos intensos y 255 para los que tienen mayor intensidad)
            filteredImg = cv.normalize(img, None, alpha=value+1, beta=-value, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
            
        elif (value < 0): 
            # valor = [-1, -100]
            # alpha = [1, 0.5]
            # beta =  [0, 0.5]
            alpha = float(1 + value / 200)
            beta = float(-value / 200)
            print(alpha)
            print(beta)
            # Se normalizan los valores de los canales, acercándolos a un punto medio (128)
            filteredImg = cv.normalize(img, None, alpha=alpha, beta=beta, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
        if (value != 0):
            filteredImg = np.clip(filteredImg, 0, 1)
            filteredImg = (255*filteredImg).astype('uint8')
            

    elif (filterX == 'saturation'):             # value =            [1, 100]
        if (value > 0): value = float(value/10) # +saturación =      [1, 10]
                                                # value              [-1, -100]
        elif (value < 0): value = float(1+value/100) # -saturación = [1, 0]
        
        if (value != 0):
            # Se cambia el formato de la imagen de BGR a HSV (Hue, Saturation, Value)
            hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            # Se utiliza el valor V para modificar el brillo de cada canal
            hsvValue = hsvImg[:,:,1]
            modifiedValueChannel = np.clip(hsvValue * value, 0, 255).astype('uint8')
            hsvImg[:,:,1] = modifiedValueChannel
            filteredImg = cv.cvtColor(hsvImg, cv.COLOR_HSV2BGR) 
        
                    
    elif (filterX == 'sharpness'):
        if (value > 0):                            # value =     [1, 100]
            valueSharpness = int(10 / 100 * value) # sharpness = [1, 10]
            filteredImg = cv.GaussianBlur(img,(5,5),0)
            filteredImg = cv.addWeighted(img, valueSharpness + 1.5, filteredImg, - valueSharpness - 0.5,0)
            
        elif (value < 0):
            avg = (rows + columns)/2/10 # El filtro es máximo 1/10 las dimensiones de la imagen
            valueGauss = int(avg / 100 * (value * -1)) 
            if (valueGauss % 2 == 0): valueGauss += 1  # Se cambia al siguiente impar          
            filteredImg = cv.GaussianBlur(img,(valueGauss,valueGauss),0)
        
        
    elif (filterX == 'red' or filterX == 'green' or filterX == 'blue'):
        value = int(255 / 100 * value)
        
        # Se obtienen los canales de color
        redChannel=np.array(img[:,:,2],dtype='int16')
        greenChannel=np.array(img[:,:,1],dtype='int16')
        blueChannel=np.array(img[:,:,0],dtype='int16')
        
        # value =   [1 - 100]
        # channel = [2.55 - 255]
                        
        if (value > 0): # Se define un valor mínimo en canal
            if (filterX == 'red'): redChannel=np.minimum(255,redChannel+value)
            elif (filterX == 'green'): greenChannel=np.minimum(255,greenChannel+value)
            elif (filterX == 'blue'): blueChannel=np.minimum(255,blueChannel+value)

        elif (value < 0): # Se define un valor máximo en canal
            plainImage=np.zeros((rows,columns),dtype='uint8')
            if (filterX == 'red'): redChannel=np.maximum(plainImage,redChannel+value)
            elif (filterX == 'green'): greenChannel=np.maximum(plainImage,greenChannel+value)
            elif (filterX == 'blue'): blueChannel=np.maximum(plainImage,blueChannel+value)
            
        # Se convierten los canales a 8 bits
        redChannel=redChannel.astype('uint8')
        greenChannel=greenChannel.astype('uint8')
        blueChannel=blueChannel.astype('uint8')
        filteredImg = cv.merge([blueChannel, greenChannel,redChannel]) 
            
    return filteredImg