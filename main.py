import requests, bs4, os, path

principal_page = 'https://escola-ebd.com.br/biblia/biblia-em-audio-cid-moreira/'
genesis_page = 'http://escola-ebd.com.br/biblia/genesis-em-audio/'
exodo_page = 'http://escola-ebd.com.br/biblia/exodo-em-audio/'

class Book():
    title = ''
    link = ''

class Chapter():
    title = ''
    link = ''
    
def download(url, address):
    result = requests.get(url)
    if result.status_code == requests.codes.OK:
        with open(address, 'wb') as new_file:
            new_file.write(result.content)
        print('Download finalizado!!! - {}'.format(address))
    else:
        result.raise_for_status()
        print('Não deu certo!!')

def get_link_from_books():
    books = []

    result = requests.get(principal_page)
    html = bs4.BeautifulSoup(result.text, features='html.parser')
    #html = bs4.BeautifulSoup(tree.prettify())

    for item in html.select('.page_item h3 span a'):
        book = Book()
        book.link = item.get('href')
        book.title = item.get_text().upper()
        books.append(book)
    
    return books

def get_link_from_chapters(link, folder):
    chapters = []
    
    result = requests.get(link)
    tree = bs4.BeautifulSoup(result.text, features='html.parser')
    html = tree.prettify()
    html = bs4.BeautifulSoup(html, features='html.parser')
    
    for item in html.select('#main article div div a'):
        chapter = Chapter()
        chapter.link = item.get('href')
        chapter.title = item.get_text().rstrip().lstrip().strip()
        chapters.append(chapter)
        
    for item in chapters:
        
        download(item.link, './{}/{}.mp3'.format(folder, item.title))
    

books = get_link_from_books()

for i in range(len(books)):
    folder = './{} - {}'.format(i+1, books[i].title)
    print(folder)
    if os.path.isdir(folder):
        print('é uma pasta')
    else:
        os.mkdir(folder)
        print('A pasta {} foi criada com sucesso!!'.format(folder))
    
    get_link_from_chapters(books[i].link, folder)
    

