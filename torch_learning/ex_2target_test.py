import torch
import torch.nn as nn
import torchvision
from torchvision import transforms, utils
import matplotlib.pyplot as plt
import os
import numpy as np
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from torchvision.utils import save_image

path='D:/PYTHON/螺桿單元'

#path='D:/PYTHON/螺桿單元-外插2'
# normalize or not     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
img_data = torchvision.datasets.ImageFolder(path,
                                            transform=transforms.Compose([
                                                transforms.Scale(32),
                                                transforms.CenterCrop(28),
                                                transforms.ToTensor(),
                                                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                                ])
                                            )
print(img_data.imgs)
#print(len(img_data))
#print(len(data_loader))
print(img_data.class_to_idx)

img_loader = torch.utils.data.DataLoader(img_data, batch_size=30, num_workers=0,shuffle=False)

images,labels=next(iter(img_loader))
print(images.shape)
print(labels.shape)

classes=[
    'kL1-50-4', 'kL2-50-4', 'kL3-50-4', 'kR1-50-4', 'kR2-50-4', 'kR3-50-4',\
    'mL1c-50-15', 'mL1r-50-15', 'mL1t-50-15', 'mL2c-50-15', 'mL2r-50-15',\
    'mL2t-50-15', 'mL3c-50-15', 'mL3r-50-15', 'mL3t-50-15', 'mR1c-50-15',\
    'mR1r-50-15', 'mR1t-50-15', 'mR2c-50-15', 'mR2r-50-15', 'mR2t-50-15',\
    'mR3c-50-15', 'mR3r-50-15', 'mR3t-50-15', 'sL1-50-33', 'sL2-50-33',\
    'sL3-50-33', 'sR1-50-33', 'sR2-50-33', 'sR3-50-33'
]
#classes=['sL3-50-33']
def imshow(img):
    img = img.permute(1,2,0)
    img = torch.clamp(img,0,1)
    plt.imshow(img)
   
dataiter = iter(img_loader)
images, labels = dataiter.next()

# plot the images in the batch, along with the corresponding labels
fig = plt.figure(figsize=(25, 30))

for idx in np.arange(29):
    ax = fig.add_subplot(6, 5, idx+1, xticks=[], yticks=[])
    imshow(images[idx])
    ax.set_title("{} ".format( classes[labels[idx]]),fontsize=10)
plt.show()

class CNNAE(nn.Module):
    def __init__(self):
        super(CNNAE, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=3, padding=1),  #(16,10,10)
            nn.BatchNorm2d(16),
            nn.Tanh(),
            nn.MaxPool2d(2, stride=2)
        )  # 16,5,5
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 4, 3, stride=2, padding=1),  # 
            nn.BatchNorm2d(4),
            nn.Tanh(),
            nn.MaxPool2d(2, stride=1)  #(2,2,2)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(4, 16, 3, stride=2),  # 
            nn.BatchNorm2d(16),
            nn.Tanh(),
            nn.ConvTranspose2d(16, 8, 5, stride=3, padding=1),  # 
            nn.BatchNorm2d(8),
            nn.Tanh(),
            nn.ConvTranspose2d(8, 3, 2, stride=2, padding=1),  # 
            nn.BatchNorm2d(3),
            nn.Tanh()
            
          
        )

    def forward(self, x):
        feature_map= self.conv1(x)
        encode = self.conv2(feature_map)
        decode = self.decoder(encode)
        return feature_map, encode, decode

#### Def some fxn for diagram       
def matplotlib_imshow(img, one_channel=False):
    if one_channel:
        img = img.mean(dim=0)
    npimg = img.numpy()
    if one_channel:
        plt.imshow(npimg, cmap="Greys")
    else:
        plt.imshow(np.transpose(npimg, (1, 2, 0)))

def to_img(x):
    #x = 0.5 * (x + 1)
    x = x.clamp(0, 1)
    x = x.view(x.size(0), 3, 28, 28)
    return x
def to_img2(x):
    #x = 0.5 * (x + 1)
    x = x.clamp(0, 1)
    x = x.view(x.size(0)*16, 1, 5, 5)
    return x

def to_img3(x):
    #x = 0.5 * (x + 1)
    x = x.clamp(0, 1)
    x = x.view(x.size(0)*4, 1, 2, 2)
    return x


print(len(img_loader))
model2 = CNNAE()
model2.load_state_dict(torch.load('D:/PYTHON/  CNNstd.pth'))
criterion = nn.MSELoss()

for i, (img, labels) in enumerate(img_loader):
    feature, encode , output = model2(img)
    loss = criterion(output, img)

print(loss)
pic = to_img(output)
save_image(pic, './img_test/image_{}.png'.format(1))


a=encode.view(-1,16)
b=a.detach().numpy()
#print(b)
#print(b[20])

encode_list={}
i=0
for item in classes:
    encode_list[item]=b[i]
    i += 1

#print(encode_list)


def text_to_encode(item):
#     tmp = item.split('-')
    onehot_data = encode_list[item]
    return onehot_data

#Part1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter


### function of data normalization
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

def min_max_normalize(my_matrix):
    scaler = MinMaxScaler()
    scaler.fit(my_matrix)
    my_matrix_normorlize=scaler.transform(my_matrix)
    return my_matrix_normorlize

def normalize(my_matrix):
    scaler = preprocessing.StandardScaler().fit(my_matrix)
    my_matrix_normorlize=scaler.transform(my_matrix)
    return my_matrix_normorlize

#Part3
columns = ['Rotation_speed','Total_rate','one','two','three','RTD','Temperature']
train =pd.read_csv('D:/PYTHON/外插2.csv', names=columns)
train=train.sample(frac=1)
print(len(np.array(train)))
train.head()
train.Temperature=pd.to_numeric(train.Temperature)

#Part4
### normalize speed
speed = np.array([train.Rotation_speed.values],dtype = np.float32).transpose(1,0)
print(speed.shape)
speed_min = min_max_normalize(speed)
print(speed_min[:4])
speed_nor = normalize(speed)
# print(speed_nor[:4])

### normalize total rate
Total_rate = np.array([train.Total_rate.values],dtype = np.float32).transpose(1,0)
print(Total_rate.shape)
Total_rate_min = min_max_normalize(Total_rate)
print(Total_rate_min[:4])
Total_rate_nor = normalize(Total_rate)
# print(speed_nor[:4])

#Part5
### get the text_onehot_list for transfer string to one-hot vector
train_one = np.concatenate((train.one.values,train.two.values,train.three.values))
# test_one = np.concatenate((test.one.values,test.two.values,test.three.values))

#Part6
### prepare the training data
quantity = np.concatenate((speed_min,Total_rate_min),1)
#print(quantity.shape)
# (3140,2)
train_y = np.concatenate((np.array([train.RTD.values]).transpose(1,0),
                         np.array([train.Temperature.values]).transpose(1,0)),axis = 1)

#print(train_y.shape)
# (3140,2)
train_one = np.array(train.one.values)
train_two = np.array(train.two.values)
train_three = np.array(train.three.values)

test_yR = train_y[0:327,0:2]
std2_test_yR=normalize(test_yR)

#print(len(test_y),test_y.shape)
# (340,2)

test_quantity = quantity[0:327,:]
#print(test_quantity.shape)
# (340,2)

test_one = train_one[0:327]
test_two = train_two[0:327]
test_three = train_three[0:327]


import torch
import torch.nn as nn
import torch.utils.data as Data
import torchvision


class AutoEncoder(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(AutoEncoder, self).__init__()
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.output_size = output_size
        # 压缩
        self.encoder = nn.Sequential(
#             nn.Linear(5, 32),
            nn.Linear(input_size, hidden_size),
            nn.Tanh(),
#             nn.Linear(15, 15),
#             nn.Tanh(),
#             nn.Linear(15, 15),
#             nn.Tanh(),
#            nn.Linear(hidden_size, 1),   # 压缩成3个特征, 进行 3D 图像可视化
#             nn.Tanh(),
        )
        self.encoder2 = nn.Linear(hidden_size, 1)
        # 解压
        self.decoder = nn.Sequential(
            nn.Linear(1, hidden_size),
            nn.Tanh(),
#             nn.Linear(15, 15),
#             nn.Tanh(),
#             nn.Linear(15, 15),
#             nn.Tanh(),
            nn.Linear(hidden_size,output_size),
#             nn.Sigmoid(),       # 激励函数让输出值在 (0, 1)
        )

    def forward(self, x):
        feature = self.encoder(x)
        encoded =  self.encoder2(feature)
        decoded = self.decoder(encoded)
        return feature, encoded, decoded

class Extrader(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Extrader, self).__init__()
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.output_size = output_size
        # 压缩
        self.model = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.Dropout(0.5),
            nn.Tanh(),
            nn.Linear(64, 64),#
            nn.Dropout(0.5),
            nn.Tanh(),
            nn.Linear(64, 64),#
            nn.Dropout(0.5),
            nn.Tanh(),#
            nn.Linear(64, output_size),   # 压缩成3个特征, 进行 3D 图像可视化
        )
        
    def forward(self, x):
        return(self.model(x))


#Part9
class IntegratedModel(nn.Module):
    def __init__(self):
        super(IntegratedModel, self).__init__()
        self.AE = AutoEncoder(16,8,16)
        self.extrater = Extrader(5,64,2)
        
        
    def forward(self, quality, quantity):
        feature1, encoded_1,decoded_1 = self.AE(quality[0].unsqueeze(0))
#         print(encoded_1.shape)
        feature2, encoded_2,decoded_2 = self.AE(quality[1].unsqueeze(0))
        feature3, encoded_3,decoded_3 = self.AE(quality[2].unsqueeze(0))
#         print(quantity[0,0].shape)
        input_value = torch.cat((encoded_1, encoded_2,
                                 encoded_3,quantity),1)
#         print(input_value.shape)
        out = self.extrater(input_value)
        return feature1,feature2,feature3,decoded_1,decoded_2,decoded_3,out
my_model2 = IntegratedModel()
my_model2.load_state_dict(torch.load('D:/PYTHON/  NNmodel_2target_std2.pth'))
loss_func = nn.MSELoss()
writer = SummaryWriter('2targetSTD_ex2/NN_result')

for epoch in range(1):
    total_loss1 = 0
    total_loss2 = 0
    tensor_list = [] #存放数据tensor
    meta_data = [] #存放标签
    features = torch.zeros(0)
    for i in range(len(test_yR)):
        
        ### train AE
        targetR = torch.FloatTensor(std2_test_yR[i]).view(1,-1).detach()
        en_input1 = torch.FloatTensor(text_to_encode(test_one[i])).unsqueeze(0)
        en_input2 = torch.FloatTensor(text_to_encode(test_two[i])).unsqueeze(0)
        en_input3 = torch.FloatTensor(text_to_encode(test_three[i])).unsqueeze(0)
        x = torch.cat((en_input1,en_input2,en_input3),0)
        y = torch.FloatTensor(test_quantity[i]).unsqueeze(0)
        f1,f2,f3,d1,d2,d3,outR = my_model2(x,y)
        
        loss = loss_func(d1, en_input1) + loss_func(d2, en_input2) + loss_func(d3, en_input3)
        total_loss1 += loss.item()
        loss1 = total_loss1/327
        
        ### train extrater
        targetR = torch.FloatTensor(std2_test_yR[i]).view(1,-1).detach()
        en_input1 = torch.FloatTensor(text_to_encode(test_one[i])).unsqueeze(0)
        en_input2 = torch.FloatTensor(text_to_encode(test_two[i])).unsqueeze(0)
        en_input3 = torch.FloatTensor(text_to_encode(test_three[i])).unsqueeze(0)
        x = torch.cat((en_input1,en_input2,en_input3),0)
        #print(x.shape)
        y = torch.FloatTensor(test_quantity[i]).unsqueeze(0)
        #print(y.shape)
        f1,f2,f3,d1,d2,d3,outR = my_model2(x,y)
        #print(input_value.shape)#  1,50
        
        loss = loss_func(outR, targetR)
        print(loss)
        total_loss2 += loss.item()
        loss2 = total_loss2/327

        features = torch.cat((features, f1))
        features = torch.cat((features, f2))
        features = torch.cat((features, f3))
        label1=[str(train_one[i])]
        label2=[str(train_two[i])]
        label3=[str(train_three[i])]
        meta_data.append(label1)
        meta_data.append(label2)
        meta_data.append(label3)
        #writer.add_scalar('MSE_loss', loss, i)

    print(loss1)
    print(loss2)
    features = features.view(-1, 8)
    writer.add_embedding(features, metadata=meta_data, global_step=epoch)