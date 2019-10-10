import torch
import logging
import models.modules.SRResNet_arch as SRResNet_arch
import models.modules.discriminator_vgg_arch as SRGAN_arch
import models.modules.RRDBNet_arch as RRDBNet_arch
from models.modules.InvSimpleNet_arch import *
from models.modules.Inv_arch import InvSRNet, InvExpSRNet
from models.modules.Subnet_constructor import subnet
import math
logger = logging.getLogger('base')


####################
# define network
####################
#### Generator
def define_G(opt):
    opt_net = opt['network_G']
    which_model = opt_net['which_model_G']
    if opt_net['init']:
        init = opt_net['init']
    else:
        init = 'kaiming'

	#if which_model == 'MSRResNet':
	#    netG = SRResNet_arch.MSRResNet(in_nc=opt_net['in_nc'], out_nc=opt_net['out_nc'],
	#                                   nf=opt_net['nf'], nb=opt_net['nb'], upscale=opt_net['scale'])
	#elif which_model == 'RRDBNet':
	#    netG = RRDBNet_arch.RRDBNet(in_nc=opt_net['in_nc'], out_nc=opt_net['out_nc'],
	#                                nf=opt_net['nf'], nb=opt_net['nb'])
    # elif which_model == 'sft_arch':  # SFT-GAN
    #     netG = sft_arch.SFT_Net()
    if which_model == 'InvSimpleNet':
        upscale_log = int(math.log(opt_net['scale'], 2))
        #netG = InvSimpleNet(opt_net['in_nc'], opt_net['out_nc'], opt_net['block_num'], upscale_log)
        netG = InvSRNet(opt_net['in_nc'], opt_net['out_nc'], subnet('SimpleNet', init), opt_net['block_num'], upscale_log)
    elif which_model == 'InvExpSimpleNet':
        upscale_log = int(math.log(opt_net['scale'], 2))
        netG = InvExpSRNet(opt_net['in_nc'], opt_net['out_nc'], subnet('SimpleNet', init), opt_net['block_num'], upscale_log)
    elif which_model == 'InvExpTHNet':
        upscale_log = int(math.log(opt_net['scale'], 2))
        netG = InvExpSRNet(opt_net['in_nc'], opt_net['out_nc'], subnet('THNet', init), opt_net['block_num'], upscale_log)
    elif which_model == 'InvSigmoidSimpleNet':
        upscale_log = int(math.log(opt_net['scale'], 2))
        netG = InvSigmoidSRNet(opt_net['in_nc'], opt_net['out_nc'], subnet('SimpleNet', init), opt_net['block_num'], upscale_log)
    elif which_model == 'InvExpSigmoidSimpleNet':
        upscale_log = int(math.log(opt_net['scale'], 2))
        netG = InvExpSigmoidSRNet(opt_net['in_nc'], opt_net['out_nc'], subnet('SimpleNet', init), opt_net['block_num'], upscale_log)
    else:
        raise NotImplementedError('Generator model [{:s}] not recognized'.format(which_model))
    return netG


#### Discriminator
def define_D(opt):
    opt_net = opt['network_D']
    which_model = opt_net['which_model_D']

    if which_model == 'discriminator_vgg_128':
        netD = SRGAN_arch.Discriminator_VGG_128(in_nc=opt_net['in_nc'], nf=opt_net['nf'])
    else:
        raise NotImplementedError('Discriminator model [{:s}] not recognized'.format(which_model))
    return netD


##### Define Network used for Perceptual Loss
#def define_F(opt, use_bn=False):
#    gpu_ids = opt['gpu_ids']
#    device = torch.device('cuda' if gpu_ids else 'cpu')
#    # PyTorch pretrained VGG19-54, before ReLU.
#    if use_bn:
#        feature_layer = 49
#    else:
#        feature_layer = 34
#    netF = SRGAN_arch.VGGFeatureExtractor(feature_layer=feature_layer, use_bn=use_bn,
#                                          use_input_norm=True, device=device)
#    netF.eval()  # No need to train
#    return netF
