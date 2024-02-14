'''
Não tô conseguindo fazer os type hints direito -> não queria usar bib
Quero ver qual o melhor jeito de usar flags e lidar com erros no python (seguir o padrão do Google)

Lembrei que o python tem o try/except, acho que é assim que lida com erros

Para acompanhar melhor vou anotar aqui:
    O programa segue um raciocínio onde para fazer o pdf ele precisa da imagem (já no tamanho correto) e da posição superior esquerda de cada uma das imagens,
    Assim, seguimos os seguintes raciocínios para cada um dos métodos:
        1 - Como o tamanho da imagem já é decidido, fazemos que a quantidade de colunas é dada pela aproximação para baixo do comprimento do pdf dividido pelo comprimento da imagem, o mesmo deve ser feito para a quantidade de linha, porém usando a altura. Após isso teremos a disposição das imagens e as imagens em si, basta inserir as imagens no meio de cada região.

        2 - Sabendo a disposição das imagens precisamos saber o tamanho que elas devem ter. Nesse ponto sabemos o tamanho máximo que as imagens podem ocupar (é dado pelo tamanho máximo do pdf em cada um dos eixos dividido pela quantidade de imagens em cada um dos eixos) então, para comportar a imagem maior possível em cada espaço avaliamos a proporção (comprimento/altura) do espaço e da imagem, se ambos forem maiores do 1 então o comprimento da imagem deve ser igual ao do espaço (a altura é ajustada de forma a manter a proporção), caso ambos sejam menores do que 1 então a altura da imagem deve ser igual à do espaço, se um deles for maior do que 1 e o outro menor, a imagem deve ser rotacionada em 90 graus, então o padrão se repete.

        3 - 

- [ ] Reavaliar os métodos de geração de imagem
- [ ] Separar o processo em mais funções
- [ ] Otimizar as funções
- [ ] Inserir comentários e envio de erros nas funções
- [ ] Lidar com os erros na main()
- [ ] Testar todo o processo com casos variados
- [ ] Seria interessante adicionar um offset (espaço em branco) opcional
- [ ] Adicionar também linhas opcionais dividindo as imagens
'''

from PIL import Image

#razão pixel/centimetro = 118.1056

#------Definição de Flags------#
SUCESS = 0
UNEXPECTED_ERROR = 1
IMAGE_SIZE_ERROR = 2
IMAGE_NOT_FOUND = 3
INVALID_NUMBER = 4
FUNCTION_INPUT_ERROR = 5
TYPE_ERROR = 6

def test() -> int:

    pos = [0,0]
    tam = [5,5]

    print(getCenter(pos,tam))

    return 0

def main() -> int:
    
    #--------Criando o PDF--------#
    white = (255,255,255)
    pdfSize = [2480, 3508] #tamanho de um pdf em pixels
    pdf = Image.new(mode="RGB",size=pdfSize, color=white)

    #-------Pegando a Imagem---------#
    print("Antes de começar, tenha certeza de que o programa está sendo executado na mesma pasta onde está a imagem que você quer colocar")
    nome = input("Insira o nome da imagem que quer colocar (não esqueça da extensão, como png,jpeg,etc):")
    print("\n")
    try:
        img = Image.open(nome)
        imgSize = list(img.size)
    except:
        return IMAGE_NOT_FOUND

    #---------Escolhendo Método-------#
    print("Por enquanto existem apenas 3 métodos funcionando, espero incluir mais um no futuro")
    print("Os métodos são:\n")
    print("1 - É inserida a maior quantidade de imagens possível sem alterar o tamanho dela, ideal para quando a imagem já está no tamanho correto")
    print("2 - Você insere a proporção das imagens, o tamanho da imagem pode ser alterado para que ela se encaixe na proporção desejada, mas ainda assim ela terá o tamanho máximo para a proporção dada.")
    print("3 - Você insere o tamanho desejado para a imagem e será criado um pdf com a maior quantidade de imagens nesse tamanho")
    method = int(input("Insira o número do método que você deseja:")) #Acho que não precisa colocar a opção de imprimir novamente
    if method == 2:
        prop = input("Insira a proporção, com os números separados por um espaço\n")
        prop = list(map(int,prop.split()))
        finalPdf = proportion(prop,img,imgSize,pdf,pdfSize)
    if method == 1:
        finalPdf = standart(pdf,pdfSize,img,imgSize)
    if method == 3:
        size = input("Insira o tamanho da imagem em pixels e separado com um espaço\n")
        size = list(map(int,size.split()))
        finalPdf = ImageSize(size,pdf,pdfSize,img,imgSize)
    print('')
    print("Tudo feito!\nSeu PDF foi criado com o nome 'result.pdf' na mesma pasta da imagem")
    finalPdf.save('result.pdf')

    return SUCESS

def getCenter(pos: tuple,tam: tuple):
    '''Recebe:

        - pos:(lista) posição x e y de onde está a figura
        - tam:(lista) tamanho da imagem

        Retorna:

        - (lista) [posição x,posição y]
        Arredonda a posição para baixo (valor inteiro de pixels)
    '''
    if len(pos) == 2 & len(tam) == 2:
        if type(pos[0]) == int & type(pos[1]) == int & type(tam[0]) == int & type(tam[1]) == int: #Otimizar isso se possível
            return [round(pos[0] + tam[0]/2),round(pos[1] + tam[1]/2)]
        else:
            return TYPE_ERROR
    else:
        return FUNCTION_INPUT_ERROR

def resizeImage(gridSize,img,imgSize): #Otimizar isso
    '''Recebe:

        - 
        - 
        - 

        Retorna:

        - 
    '''
    imgR = imgSize[0]/imgSize[1]
    if imgSize[0] > gridSize[0]:
        imgSize[0] = int(gridSize[0])
        imgSize[1] = int(imgSize[0]/imgR)
    if imgSize[1] > gridSize[1]:
        imgSize[1] = int(gridSize[1])
        imgSize[0] = int(imgR*imgSize[1])
    return img.resize(tuple(imgSize)),imgSize

def makePDF(grid,gridSize,pdf,img,imgSize):
    '''Recebe:
        - grid (lista): lista com o conjuntos de pontos onde serão colocadas as imagens
        - pdf: Arquivo do pdf
        - img: Arquivo da imagem

        Retorna:
        - Arquivo do pdf com as imagens adicionadas
    '''
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

#-------Funções não implementadas-------#
'''Vou escrever aqui umas funções que seriam uteis mas não vou implementar agora porque não tenho a documentação do pilow'''

def rotateImage(img,turn,degres): #Ver qual o equivalente no pilow
    pass

def positionImageCenter(imgSize,gridSize):
    '''Recebe:

        - imgSize (lista): comprimento e altura da imagem
        - gridSize (lista): comprimento e altura do espaço onde a imagem será colocada

        Retorna:
        - Posição (canto superior esquerdo) onde deve ser colocada a imagem para que ela esteja no meio do espaço
    '''
    if(len(imgSize) != 2 or len(gridSize) != 2):
        return INVALID_NUMBER
    elif (type(imgSize[0] != int or type(imgSize[1]) != int or type(gridSize[0]) != int or type(gridSize[1]) != int)):
        return TYPE_ERROR
    elif (imgSize[0] > gridSize[0] or imgSize[1] > gridSize[1]):
        return IMAGE_SIZE_ERROR
    else:
        x = (gridSize[0] - imgSize[0])/2
        y = (gridSize[1] - imgSize[1])/2
        return [x,y]

if __name__ == '__main__':
    #flag = test()
    main()
