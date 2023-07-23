from PIL import Image

def main() -> int:
    
    #--------Criando o PDF--------#
    white = (255,255,255)
    pdfSize = [2480, 3508] #tamanho de um pdf em pixels
    pdf = Image.new(mode="RGB",size=pdfSize, color=white)

    #-------Pegando a Imagem---------#
    print("Antes de começar, tenha certeza de que o programa está sendo executado na mesma pasta onde está a imagem que você quer colocar")
    nome = input("Insira o nome da imagem que quer colocar (não esqueça da extensão, como png,jpeg,etc):")
    print("\n")
    img = Image.open(nome)
    imgSize = list(img.size)

    print("Por enquanto existem apenas 3 métodos funcionando, espero incluir mais um no futuro")
    print("Os métodos são:\n")
    print("1-Você insere a proporção das imagens, por exemplo, se quiser 3 na vertical e 4 na horizontal você deve inserir '4 3'. O tamanho da imagem pode ser alterado para que ela se encaixe na proporção desejada, mas ainda assim ela terá o tamanho máximo para a proporção dada",
          "2-É o método padrão, ele coloca a maior quantidade de imagens possível sem alterar o tamanho dela, ideal para quando a imagem já está no tamanho correto",
          "3-Você insere o tamanho da imagem (em pixels por enquanto) na forma 'comprimento altura' e será criado um pdf com a maior quantidade de imagens nesse tamanho",
          sep='\n\n')
    method = int(input("Insira o número do método que você deseja:"))
    if method == 1:
        prop = input("Insira a proporção, com os números separados por um espaço\n")
        prop = list(map(int,prop.split()))
        finalPdf = proportion(prop,img,imgSize,pdf,pdfSize)
    if method == 2:
        finalPdf = standart(pdf,pdfSize,img,imgSize)
    if method == 3:
        size = input("Insira o tamanho da imagem em pixels e separado com um espaço\n")
        size = list(map(int,size.split()))
        finalPdf = ImageSize(size,pdf,pdfSize,img,imgSize)
    print('')
    print("Tudo feito!\nSeu PDF foi criado com o nome 'result.pdf' na mesma pasta da imagem")
    finalPdf.save('result.pdf')

    return 0

def getCenter(pos,tam):
    '''Manda o centro da figura'''
    assert len(pos) == 2
    assert len(tam) == 2
    return [pos[0] + tam[0]/2,pos[1] + tam[1]/2]

def resizeImage(gridSize,img,imgSize): #Otimizar isso
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

def proportion(prop,img,imgSize,pdf,pdfSize):
    gridSize = [pdfSize[0]/prop[0],pdfSize[1]/prop[1]]
    grid = []
    for i in range(prop[0]):
        for j in range(prop[1]):
            grid.append([i*pdfSize[0]/prop[0],j*pdfSize[1]/prop[1]])
    
    finalImg,finalImgSize = resizeImage(gridSize,img,imgSize)

    return makePDF(grid,gridSize,pdf,finalImg,finalImgSize)

def quant(quant,pdf,pdfSize,img,imgSize):
    pass

def standart(pdf,pdfSize,img,imgSize):
    prop = [pdfSize[0]//imgSize[0],pdfSize[1]//imgSize[1]]
    return proportion(prop,img,imgSize,pdf,pdfSize)

def ImageSize(newSize,pdf,pdfSize,img,imgSize):
    newImg = img.resize(tuple(newSize))
    return standart(pdf,pdfSize,newImg,newSize)

if __name__ == '__main__':
    main()