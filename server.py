import http.server
import socketserver
import termcolor
import requests, sys
from Seq import Seq

PORT = 8000





class TestHandler(http.server.BaseHTTPRequestHandler):



    def do_GET(self):



        # Printing the request line

        reqpath = self.path

        termcolor.cprint(reqpath, 'blue')

        try:
            contents=""
            if reqpath == '/main_page' or reqpath == '/': # Main menu appears
                with open("main_page.html", "r") as f:
                    contents = f.read()
                    f.close()

            elif self.path.startswith('/listSpecies'): # List Species menu appears
                with open("list_species.html", "r") as f:
                    contents = f.read()
                    f.close()

                    if self.path.startswith('/listSpecies?limit='): # In the case that the user introduce a limit
                        server = "http://rest.ensembl.org"

                        ext = "/info/species?"

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        info = r.json()

                        species = info['species']

                        msg_split = self.path.split('=')
                        limit = msg_split[1]
                        if limit.isalpha(): # If it's not a number, an error page appears
                            f = open("error.html", 'r')
                            contents = f.read()
                        else:
                            with open("species_limit.html", "r") as f:# If the limit is a number (if it is bigger than the number of species, all the species will appear)
                                contents = f.read()                   # If the limit indicated is 0, all species will appear as cero limit means no limit.
                                var = ''
                                lim = 0
                                for i in species:
                                    lim += 1 #To control the limit
                                    var += i['name'] + '<p>' #To store the species
                                    if str(lim) == limit: #It stops when the limit is reached
                                        break

                                sentence = 'List of species: ' + '<p>' + var
                                contents = contents.replace('#', sentence) # Receplace the info asked for in the html page



            elif self.path.startswith('/karyotype'):
                with open("karyotype.html", "r") as f: # Karyotype menu appears
                    contents = f.read()
                    f.close()

                    if self.path.startswith('/karyotype?species='): # When a specie is requested

                        msg_split = self.path.split('=')

                        server = "http://rest.ensembl.org"

                        ext = "/info/assembly/{}?".format(msg_split[1])

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        info = r.json()

                        karyotype = info['karyotype']
                        with open("karyotype_limit.html", "r") as f: # Result page of the karyotype asked for is opened
                            contents = f.read()
                            var = ''
                            for i in karyotype:
                                var += i + ' '

                            sentence = 'The karyotype of ' + msg_split[1] + ' is: ' + var
                            contents = contents.replace('#', sentence) # Replace the information in the return html page



            elif self.path.startswith('/chromosomeLength'):
                with open("chromosome_lenght.html", "r") as f: # Chromosome Length menu page
                    contents = f.read()
                    f.close()
                    if self.path.startswith('/chromosomeLength?specie='): #When a chromose of a specie is asked

                        msg_split = self.path.split('=')

                        msg_split2 = []

                        for i in msg_split:
                            msg_split2 += i.split('&')

                        server = "http://rest.ensembl.org"

                        ext = "/info/assembly/{}?".format(msg_split2[1])

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        information = r.json()

                        chromo = msg_split2[3]

                        for i in information['top_level_region']:

                            if chromo == i['name']:
                                length = i['length']

                                with open("chromo_limit.html", "r") as f: #Result page is opened
                                    contents = f.read()
                                    sentence = 'The length of the chromosome ' + chromo + ' of the species ' + msg_split2[1] + ' is: ' + str(length)
                                    contents = contents.replace('#', sentence)



            elif self.path.startswith('/geneSeq'): #Gene sequence menu page
                with open("gene_seq.html", "r") as f:
                    contents = f.read()
                    f.close()

                    if self.path.startswith('/geneSeq?gene='): #When the user select a gene
                        msg_split = self.path.split('=')

                        server = "http://rest.ensembl.org"

                        ext = "/lookup/symbol/homo_sapiens/{}?".format(msg_split[1])

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        info = r.json()
                        name=''
                        if msg_split[1] == info['display_name']:
                            name = info['id']

                        server = "http://rest.ensembl.org"

                        ext = "/sequence/id/{}?".format(name)

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        info = r.json()

                        gene_sequence = info['seq']

                        sentence = 'The sequence of the human gene ' + msg_split[1] + ' is ' + gene_sequence
                        with open("gene_seqRes.html", "r") as f: #Result page
                            contents = f.read()
                            contents = contents.replace('#', sentence)



            elif self.path.startswith('/geneInfo'): #Gene information menu page is opened
                with open("gene_info.html", "r") as f:
                    contents = f.read()
                    f.close()
                if self.path.startswith('/geneInfo?gene='):

                    msg_split = self.path.split('=')

                    server = "http://rest.ensembl.org"

                    ext = "/lookup/symbol/homo_sapiens/{}?".format(msg_split[1])

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    info = r.json()
                    name=""
                    if msg_split[1] == info['display_name']:
                        name = info['id']

                    server = "http://rest.ensembl.org"

                    ext = "/lookup/id/{}?".format(name)

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    info2 = r.json()

                    start = info2['start']

                    end = info2['end']

                    id = info2['id']

                    chromo = info2['seq_region_name']

                    with open("gene_info_gene.html", "r") as f: #Result page
                            contents = f.read()
                            len= end-start
                            text= 'The start of the human gene ' + msg_split[1] + ' is: ' + str(start) + '</p></p>' + 'The end of the human gene ' + msg_split[1] + ' is: ' + str(end) + '</p></p>' + 'The lenght of the human gene ' + msg_split[1] + ' is: ' + str(len) +'</p></p>' + 'The id of the human gene ' + msg_split[1] + ' is: ' + str(id) +'</p></p>' + 'The gen ' + msg_split[1] + ' is in  the chromosome: ' + str(chromo)
                            contents = contents.replace('#', text)




            elif self.path.startswith('/geneCalc'):
                with open("gene_calc.html", "r") as f: # Gene calculation menu page
                    contents = f.read()
                    f.close()

                if self.path.startswith('/geneCalc?gene='): #When a gene is introduced

                    msg_split = self.path.split('=')

                    server = "http://rest.ensembl.org"

                    ext = "/lookup/symbol/homo_sapiens/{}?".format(msg_split[1])

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    info = r.json()
                    name=''
                    if msg_split[1] == info['display_name']:
                        name = info['id']

                    server = "http://rest.ensembl.org"

                    ext = "/sequence/id/{}?".format(name)

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    info = r.json()

                    gene_sequence = info['seq']

                    seq = Seq(gene_sequence) # The function stored in the document Seq.py

                    length = str(seq.len())

                    percentageA = str(seq.perc('A'))
                    percentageT = str(seq.perc('T'))
                    percentageG = str(seq.perc('G'))
                    percentageC = str(seq.perc('C'))

                    sentence= 'The length of the sequence of the human gene ' + msg_split[1] + ' is: ' + length + '</p></p>'

                    per_a = 'The percentage of the base A in the sequence of the human gene: ' + msg_split[
                        1] + ' is ' + percentageA + '%' + '</p></p>'

                    per_t = 'The percentage of the base T in the sequence of the human gene: ' + msg_split[
                        1] + ' is ' + percentageT + '%' + '</p></p>'

                    per_g = 'The percentage of the base G in the sequence of the human gene: ' + msg_split[
                        1] + ' is ' + percentageG + '%' + '</p></p>'

                    per_c = 'The percentage of the base C in the sequence of the human gene: ' + msg_split[1] + ' is ' + percentageC + '%'

                    text = sentence + per_a + per_t + per_g + per_c
                    with open("gene_calResult.html", "r") as f: # Return a result page with the operations
                        contents = f.read()
                        contents = contents.replace('#', text)



            elif self.path.startswith('/geneList'): # Gene list menu page
                with open("gene_list.html", "r") as f:
                    contents = f.read()
                    f.close()

                if self.path.startswith('/geneList?chromo='): # When the data is introduced

                    msg_split = self.path.split('=')

                    msg_split2 = []

                    for i in msg_split:
                        msg_split2 += i.split('&')

                    server = "http://rest.ensembl.org"

                    ext = "/overlap/region/human/" + str(msg_split2[1]) + ":" + msg_split2[3] + "-" + msg_split2[
                        5] + "?feature=gene"

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    inform = r.json()

                    sentence = 'The genes in the chromosome ' + msg_split2[1] + ' of the homo sapiens ' + ' between ' + msg_split2[3] + ' and ' + msg_split2[5] + ' are: '
                    for i in inform:
                        sentence += '<p>' + i['external_name'] + '<p>'

                    with open("gene_listRes.html", "r") as f: # Return page for the information asked for
                            contents = f.read()
                            contents = contents.replace('#', sentence)



            self.send_response(200)  # Status line: OK!

            # Define the content-type header:

            self.send_header("Content-Type", "text/html\r\n")

            # The header is finished

            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))

            return



        except KeyError: # In the case that an error occurs. For example: the specie is not in the data, the input must be a nuber but the user introduce letters...
            f = open('error.html', 'r')
            contents = f.read()

            self.send_response(200)  # -- Status line: OK!

            # Define the content-type header:
            self.send_header("Content-Type", "text/html\r\n")

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))

        except TypeError: # In the case that an error occurs. The input is not correct, black spaces...
            f = open('error.html', 'r')
            contents = f.read()

            self.send_response(200)  # -- Status line: OK!

            # Define the content-type header:
            self.send_header("Content-Type", "text/html\r\n")

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))








#  Main program

socketserver.TCPServer.allow_reuse_address = True # Given by the professor for avoiding the PORT in use error
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:

    print("Serving at PORT:  {}".format(PORT))



    try:

        httpd.serve_forever()

    except KeyboardInterrupt:

        httpd.server_close()



print("The server is stopped")