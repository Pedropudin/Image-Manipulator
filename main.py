from PIL import Image

def main() -> int:
    
    #--------Criando o PDF--------#
    white = (255,255,255)
    pdfSize = [2480, 3508] #tamanho de um pdf em pixels
    pdf = Image.new(mode="RGB",size=pdfSize, color=white)

    #-------Pegando a Imagem---------#
    #print("Antes de começar, tenha certeza de que o programa está sendo executado na mesma pasta onde está a imagem que você quer colocar")
    #nome = input("Insira o nome da imagem que quer colocar (não esqueça da extensão, como png,jpeg,etc):")
    nome = "bird.jpeg" #apagar isso depois, só pra teste
    #print("\n")
    img = Image.open(nome)
    imgSize = list(img.size)

    finalPdf = prop([5,10],img,imgSize,pdf,pdfSize)
    finalPdf.save('teste.pdf')

    """finalPDF = makePDF([(0,0),(0,pdfSize[1]//2)],(2480,3508/2),pdf,img,imgSize)
    finalPDF.save('teste.pdf')"""

    """pdfCenter = getCenter((0,0),pdfSize)
    imgCenter = getCenter((0,0),imgSize)
    imgPos = (pdfCenter[0] - imgCenter[0],pdfCenter[1] - imgCenter[1])
    print(getCenter(imgPos,imgSize),pdfCenter)"""


    return 0

def getCenter(pos,tam):
    '''Manda o centro da figura'''
    assert len(pos) == 2
    assert len(tam) == 2
    return [pos[0] + tam[0]/2,pos[1] + tam[1]/2]

def resizeImage(gridSize,img,imgSize):
    imgR = imgSize[0]/imgSize[1]
    if imgSize[0] > gridSize[0]:
        imgSize[0] = int(gridSize[0])
        imgSize[1] = int(imgSize[0]/imgR)
    if imgSize[1] > gridSize[1]:
        imgSize[1] = int(gridSize[1])
        imgSize[0] = int(imgR*imgSize[1])
    return img.resize(tuple(imgSize)),imgSize

def makePDF(grid,gridSize,pdf,img,imgSize):

    imgCenter = getCenter([0,0],imgSize)
    for pos in grid:
        pdfCenter = getCenter(pos,gridSize)
        pdf.paste(img,(int(pdfCenter[0]-imgCenter[0]),int(pdfCenter[1]-imgCenter[1])))

    return pdf

def prop(prop,img,imgSize,pdf,pdfSize):
    gridSize = [pdfSize[0]/prop[0],pdfSize[1]/prop[1]]
    grid = []
    for i in range(prop[0]):
        for j in range(prop[1]):
            grid.append([i*pdfSize[0]/prop[0],j*pdfSize[1]/prop[1]])
    
    finalImg,finalImgSize = resizeImage(gridSize,img,imgSize)

    return makePDF(grid,gridSize,pdf,finalImg,finalImgSize)


if __name__ == '__main__':
    main()