import os
import requests
import sys
import shutil



# Cette fonction affiche les site disponibles
def availaible_sites():
    url = "https://my-json-server.typicode.com/tiko69/jsonserver/websites"
    query = "id=1"
    requete = requests.get(url)
    if requete.status_code == 200:
        l = []
        i = 0
        while i < len(requete.json()):
            l.append(requete.json()[i]['website'])
            i += 1

        return l
    else:
        print("Api request fail code ", requete.status_code )



# Cette fonction récupère le numéro du site choisi
def conversion(k):
    list_of_sites = availaible_sites()
    match = k
    for index, i in enumerate(list_of_sites):
        if i == match:
            return index
        



def Directory_Creation_and_copy(k, converted):
    cwd = os.getcwd() # On récupère la position où l'on se trouve
    directory = os.path.splitext(k)[0] # On enlève le suffixe du dossier que l'on souhaite créer
    path = os.path.join(cwd, directory)  # Création du chemin pour le dossier
    os.mkdir(path) # Création du sossier

    src = os.path.join(cwd, "templates/index.html") # Création de la source pour la copie
    dest = os.path.join(path, "index.html")     # Création de la destination pour la copie
    shutil.copyfile(src, dest)  # Copie de la source vers la destination

    list_of_source_content = ["[title]", "[body.color]", "[h1.background-color]", "[h1.color]", "[h1.text]", "[p.color]", "[p.text]", "[img.src]", "[img.alt]"]
    list_of_destination_content = get_website_info(converted)  
    return dest
    
    
    

def get_website_info(converted):
    list_of_query_1 = ["title", "body", "h1", "h1", "h1", "p", "p", "img", "img"]
    list_of_query_2 = [None, "color", "background-color", "color", "text", "color", "text", "src", "alt"]
    url = "https://my-json-server.typicode.com/tiko69/jsonserver/website"
    requete = requests.get(url)
    website = converted
    if requete.status_code == 200:
        l = []
        i = 0
        for i, v in zip(list_of_query_1, list_of_query_2):
            if v is None:
                l.append(requete.json()[website][i])
                #print(resultat)
            else:
                l.append(requete.json()[website][i][v])    
        return l
    else:
        print("Api request fail code ", requete.status_code )
        
# Remplace les valeurs du template de l'index par les valeurs de l'index du site choisi
def replace_index(dest, list_of_web_site_info):
    list_of_source_content = ["[title]", "[body.color]", "[h1.background-color]", "[h1.color]", "[h1.text]", "[p.color]", "[p.text]", "[img.src]", "[img.alt]"]
    list_of_destination_content = list_of_web_site_info
    dest_index = dest
    with open(dest_index, 'r') as file:
        data = file.read()
        for i, v in zip(list_of_source_content, list_of_destination_content):
            data = data.replace(i, v)
    with open(dest_index, 'w') as file:
        file.write(data)
    return data
    
def copy_image(list_of_website_info):
    image = list_of_web_site_info[7]
    dossier = list_of_web_site_info[0]
    cwd = os.getcwd()
    image_directory = os.path.join(cwd, "assets/")
    src = os.path.join(image_directory, image)
    path = os.path.join(cwd, dossier)
    dest = os.path.join(path, image)
    shutil.copyfile(src, dest)
    
    return src
    
    
if __name__ == '__main__':
    list_of_sites = availaible_sites()
    print("Bonjour, voici les sites disponibles : \n")
    
    for index, i in enumerate(list_of_sites):
        print(index + 1, ":", i)
    
    selection = input("\nSelectionnez le site que vous souhaitez créer : \n")
    if int(selection) < 6:
        choice = list_of_sites[int(selection) - 1]
    else:
        print("Veuillez selectionner un chiffre compris entre 1 et 5")
    
    converted = conversion(choice)
    
    list_of_web_site_info = get_website_info(converted)
    
    dest = Directory_Creation_and_copy(choice, converted)
    
    replace_index(dest, list_of_web_site_info)
    
    copy_image(list_of_web_site_info, )
    #print(replace_index(dest, list_of_web_site_info))
    
    #print(choice, converted, dest, list_of_web_site_info)
    
    print("\nFélicitations ! Un dossier",list_of_web_site_info[0], "vient d'être créée. Ce dossier contient l'index.html et l'image correspondant au site web choisi" )