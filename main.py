from PIL import Image

def pasteImage(background,image,prop):
    assert (type(prop) == tuple or type(prop) == list) and len(prop) == 2, "A proporção de imagens não foi inserida corretamente"

    backSize = background.size
    imgSize = image.size
    space = (backSize[0]/prop[0],backSize[1]/prop[1])
    point = [(space[0]-imgSize[0])/2,(space[1]-imgSize[1])/2]
    for i in range(prop[1]):
        for j in range(prop[0]):
            background.paste(image,(int(round(point[0],0)),int(round(point[1],1))))
            point[0] += space[0]
        point[0] -= space[0]*prop[0]
        point[1] += space[1]

def imageProp(tamPdf,prop,tamImg): #Acho que essa não é uma boa função para ter implementada
    '''Recebe o tamanho da imagem, do pdf e a proporção,
      e retorna o espaço de cada imagem e o tamanho que ela deve ter
    '''
    assert len(tamPdf) == 2 and type(tamPdf) == tuple, "Tem algo errado com o tamanho do pdf"
    assert len(prop) == 2 and type(prop) == tuple, "Tem algo errado com a proporção"
    assert len(tamImg) == 2 and type(tamImg) == tuple, "Tem algo errado com o tamanho da imagem"

    resize = False
    imgScale = tamImg[0]/tamImg[1]
    gridScale = (tamPdf[0]/prop[0],tamPdf[1]/prop[1])
    if tamImg[0] > gridScale[0]:
        resize = True
        newTamImg = [gridScale[0],gridScale[0]/imgScale]
    if tamImg[1] > gridScale[1]:
        resize = True
        newTamImg = [gridScale[1]*imgScale,gridScale[1]]
    
    if resize:
        return gridScale,newTamImg
    else:
        return gridScale,tamImg
        
def pdfCreator(pdf,grid,img):
    '''Coloca img no centro de cada grid dentro do pdf
        Retorna o pdf com as imagens
    '''
    #assert type(pdf) == Image.Image, f"Tipo do pdf está incorreto, recebeu {type(pdf)}"
    #assert type(img) == Image.Image, f"Tipo do img está incorreto, recebeu {type(img)}"
    assert type(grid) == tuple and len(grid) == 2, f"grid está incorreto"

    pdfSize = pdf.size
    imgSize = img.size
    prop = (int(round(pdfSize[0]/grid[0],0)),int(round(pdfSize[1]/grid[1],0)))
    initialPoint = [(grid[0]-imgSize[0])/2,(grid[1]-imgSize[1])/2]
    for i in range(prop[0]):
        for j in range(prop[1]):
            pdf.paste(img,(int(initialPoint[0]+(i*grid[0])),int(initialPoint[1]+(j*grid[1]))))
            print((initialPoint[0]+(i*grid[0]),initialPoint[1]+(j*grid[1])))

    pdf.save('t.pdf') #talvez colocar isso em outra função?

    return pdf



#--------Criando o PDF--------#
white = (255,255,255)
pdfSize = (2480, 3508) #tamanho de um pdf em pixels
pdf = Image.new(mode="RGB",size=pdfSize, color=white)

#-------Pegando a Imagem---------#
#print("Antes de começar, tenha certeza de que o programa está sendo executado na mesma pasta onde está a imagem que você quer colocar")
#nome = input("Insira o nome da imagem que quer colocar (não esqueça da extensão, como png,jpeg,etc):")
nome = "bird.jpeg" #apagr isso depois, só pra teste
print("\n")
img = Image.open(nome)
imgSize = img.size

#---------Configurando o Tamanho da imagem e a quantidade em uma folha----------#


#---------Métodos----------#

print(imgSize)
print(pdfSize)

pdfCreator(pdf,(pdfSize[0]/3,pdfSize[1]/3),img)