import numpy as np
import matplotlib.pyplot as plt

# V1 = [np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1)]
# V2 = [np.float64(1.0513806905215946), np.float64(1.0523782584865031), np.float64(1.0523703418142822), np.float64(1.1), np.float64(1.1), np.float64(1.0870795911035132), np.float64(1.0700699158948606), np.float64(1.051301862359563), np.float64(1.0513209440000386), np.float64(1.0642389967205912), np.float64(1.077731841820923), np.float64(1.061102317956591), np.float64(1.0513176839344152), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.0738868259287362), np.float64(1.0513806231578735), np.float64(1.0715794974500423), np.float64(1.0755788273387157), np.float64(1.079315801287799), np.float64(1.0548250177755627), np.float64(1.0981935628733372), np.float64(1.0705610804754964), np.float64(1.0599840405056917), np.float64(1.0622382824466008), np.float64(1.1), np.float64(1.080257164681906), np.float64(1.0879777643933437), np.float64(1.0718427979337495), np.float64(1.0725437098757042), np.float64(1.1), np.float64(1.0539920757862522), np.float64(1.0555454637343282), np.float64(1.0550080530992578), np.float64(1.062889782915305), np.float64(1.1), np.float64(1.1), np.float64(1.0697973306411213), np.float64(1.1), np.float64(1.0513666944006883), np.float64(1.1), np.float64(1.0547382405054486), np.float64(1.1), np.float64(1.05138104759008), np.float64(1.0837306429326328), np.float64(1.0968091003367972), np.float64(1.0940741478770915), np.float64(1.0768508383962387), np.float64(1.1), np.float64(1.0537698735342478), np.float64(1.0645531592853836), np.float64(1.0723243968687497), np.float64(1.0597862866773118), np.float64(1.0513257947704193), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.0701071033607858), np.float64(1.0894803313472043), np.float64(1.1), np.float64(1.0600739470893608), np.float64(1.1), np.float64(1.0819760998866783), np.float64(1.1), np.float64(1.0907399479575484), np.float64(1.1), np.float64(1.0895610627754453), np.float64(1.0597312075877579), np.float64(1.1), np.float64(1.0590408544125087), np.float64(1.0513759102529192), np.float64(1.1), np.float64(1.1), np.float64(1.0622329266586015), np.float64(1.0906631395603306), np.float64(1.0956669008083708), np.float64(1.0574252880411674), np.float64(1.0691761863112186), np.float64(1.068111154673091), np.float64(1.061022397227876), np.float64(1.051338856356018), np.float64(1.0941814557547629), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.065893525746205), np.float64(1.0773338658924532), np.float64(1.0906900921833482), np.float64(1.082760528364004), np.float64(1.0985147897924465), np.float64(1.1), np.float64(1.1), np.float64(1.0801150952890752), np.float64(1.0982986283717606), np.float64(1.095082578913515), np.float64(1.0695618206043662), np.float64(1.0794447222605679), np.float64(1.0997762101487434)]
# V3 = [np.float64(1.0651993444641248), np.float64(1.0826274846336337), np.float64(1.0786659749295797), np.float64(1.093551458194408), np.float64(1.0627207432678414), np.float64(1.1), np.float64(1.0605791927281432), np.float64(1.1), np.float64(1.0739851093759534), np.float64(1.053885656376251), np.float64(1.1), np.float64(1.1), np.float64(1.0951145029631892), np.float64(1.0505627851846608), np.float64(1.0952438940273648), np.float64(1.0702176062441897), np.float64(1.1), np.float64(1.0790644541270085), np.float64(1.0973087492435634), np.float64(1.0640060810170162), np.float64(1.1), np.float64(1.0988172678332067), np.float64(1.074916801534921), np.float64(1.1), np.float64(1.1), np.float64(1.0879272901283945), np.float64(1.0359864224574993), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.1), np.float64(1.0354978597968212), np.float64(1.1), np.float64(1.1), np.float64(1.060227356880697), np.float64(1.0517970450546679), np.float64(1.0525900100229681), np.float64(1.0582835969798239), np.float64(1.0496026176271334), np.float64(1.0570825299419846), np.float64(1.0908160926708905), np.float64(1.042544841422861), np.float64(1.1), np.float64(1.0710580292908598), np.float64(1.1), np.float64(1.0736812531716404), np.float64(1.0354907936075253), np.float64(1.0471007673780248), np.float64(1.0708415716198962), np.float64(1.035573256407554), np.float64(1.1), np.float64(1.081371522119451), np.float64(1.0730124382475852), np.float64(1.1), np.float64(1.0577848596976007), np.float64(1.1), np.float64(1.1), np.float64(1.0655926663646282), np.float64(1.0602552874340663), np.float64(1.093353896513245), np.float64(1.1), np.float64(1.1), np.float64(1.0939485007040288), np.float64(1.0949093153748501), np.float64(1.0354569823664355), np.float64(1.1), np.float64(1.0355088144373248), np.float64(1.0354965369967075), np.float64(1.0354691856036293), np.float64(1.0844691711862553), np.float64(1.1), np.float64(1.0864017569767221), np.float64(1.0498840278362394), np.float64(1.0753913574109248), np.float64(1.0355131340798893), np.float64(1.0472969194650257), np.float64(1.0366050676152456), np.float64(1.0785220320747646), np.float64(1.1), np.float64(1.047904181953684), np.float64(1.0354775746981795), np.float64(1.0615853313007368), np.float64(1.0765377180857083), np.float64(1.0355809789102797), np.float64(1.0357658484879866), np.float64(1.0440883170365178), np.float64(1.1), np.float64(1.0752871997037492), np.float64(1.0397481256785188), np.float64(1.0625469245126207), np.float64(1.0443411638267948), np.float64(1.0355268374967759), np.float64(1.0675224222778383), np.float64(1.055377103675791), np.float64(1.1), np.float64(1.0690187853818198), np.float64(1.1), np.float64(1.0751944554680457), np.float64(1.1), np.float64(1.084035257742314)]
#
# media_V1 = []
# media_V2 = []
# media_V3 = []
# x = []
#
# print(min(V1))
# print(max(V1))
# print(min(V2))
# print(max(V2))
# print(min(V3))
# print(max(V3))

# soma_V1 = 0
# soma_V2 = 0
# soma_V3 = 0
# for i in range(len(V1)):
#     soma_V1 += V1[i]
#     soma_V2 += V2[i]
#     soma_V3 += V3[i]
#     media_V1.append(soma_V1/(i+1))
#     media_V2.append(soma_V2/(i+1))
#     media_V3.append(soma_V3/(i+1))
#     x.append(i+1)
#
# print(media_V1[-1])
# print(media_V2[-1])
# print(media_V3[-1])
#
# plt.figure(1)
# plt.plot(x, media_V1, label='Barra 1')
# plt.plot(x, media_V2, label='Barra 2')
# plt.plot(x, media_V3, label='Barra 3')
# plt.ylabel('Magnitude de tensão média[pu]')
# plt.xlabel('Tentativas')
# plt.title('Tensão média versus tentativas')
# plt.legend()
# plt.grid()
# plt.show()

load = [np.float64(0.9555557435378432), np.float64(0.955555459484458), np.float64(0.9555557835847139), np.float64(0.9555558310821652), np.float64(0.9555557770654559), np.float64(0.9555558273568749), np.float64(0.9555550599470735), np.float64(0.9555556597188115), np.float64(0.9555558171123266), np.float64(0.9555558301508427)]
pg2 = [np.float64(1.5), np.float64(1.5), np.float64(1.5), np.float64(1.5), np.float64(1.5), np.float64(1.5), np.float64(1.5), np.float64(1.5), np.float64(1.5), np.float64(1.5)]
pg3 = [np.float64(1.1038466937150955), np.float64(1.1060413749069098), np.float64(1.1050986646675351), np.float64(1.1044795368321145), np.float64(1.1039998436699177), np.float64(1.104724104916291), np.float64(1.1066896631201868), np.float64(1.103563112354477), np.float64(1.1048599596865185), np.float64(1.1044698099458294)]

print(max(load))
print(min(pg3))
print(max(pg3))
print(np.mean(pg3))