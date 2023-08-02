import numpy as np
import torch


def huber_loss(pred,label, threshold):
    
    mae = np.abs(pred-label)
    mse = 0.5 * (pred-label)**2
    
    loss_map = mae < threshold
    loss = np.where( loss_map, 
                    mse, 
                    threshold * mae - 0.5 * threshold**2 )
    
    return loss



def custom_huber(pred,label, threshold, eps=1e-6):
    
    mae = np.abs(pred-label)
    ln_loss = np.log( mae + eps)   # ln(x), 미분하면 1/x
    mse = 0.5 * (pred-label)**2  # 0.5 x^2 , 미분하면 x
    
    loss_map = ln_loss < threshold  #equal as...   mae < e^threshold 7.8xx
    loss = np.where( loss_map, 
                    mse, 
                    threshold**2  * (ln_loss - np.log(threshold) + 0.5) )
    
    loss = np.mean(loss) / 5
    return loss


def custom_huber2(pred, label, threshold, eps=1e-6):
    mae = torch.abs(pred - label)
    ln_loss = torch.log(mae + eps)  # ln(x), the derivative is 1/x

    loss_map = ln_loss < threshold  # equal as... mae < e^threshold 7.8xx
    loss = torch.where(loss_map,
                       mae,
                       threshold *(ln_loss - torch.log(torch.Tensor([threshold]).to('cuda'))+1))

    loss = loss.mean() / 5
    return loss
