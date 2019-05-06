import http.server
import socketserver
import termcolor
import requests, sys
from Seq import Seq

PORT = 8000





class TestHandler(http.server.BaseHTTPRequestHandler):



    def do_GET(self):



        # -- Printing the request line

        reqpath = self.path

        termcolor.cprint(reqpath, 'blue')

        try:
            contents=""
            if reqpath == '/main_page' or reqpath == '/':

                with open("main_page.html", "r") as f:
                    contents = f.read()
                    f.close()

            elif self.path.startswith('/listSpecies'):
                with open("list_species.html", "r") as f:
                    contents = f.read()
                    f.close()

                    if self.path.startswith('/listSpecies?limit='):

                        #PONER DE DONDE ES EL CÓDIGO
                        server = "http://rest.ensembl.org"

                        ext = "/info/species?"

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        info = r.json()

                        species = info['species']

                        msg_split = self.path.split('=')
                        limit = msg_split[1]
                        if limit.isalpha():
                            f = open("error.html", 'r')

                            contents = f.read()
                        else:
                            with open("species_limit.html", "r") as f:
                                contents = f.read()
                                var = ''
                                lim = 0
                                for i in species:
                                    lim += 1
                                    var += i['name'] + '<p>'
                                    if str(lim) == limit:
                                        break

                                sentence = 'List of species: ' + '<p>' + var
                                contents = contents.replace('#', sentence)



            elif self.path.startswith('/karyotype'):
                with open("karyotype.html", "r") as f:
                    contents = f.read()
                    f.close()

                    if self.path.startswith('/karyotype?species='):

                        msg_split = self.path.split('=')

                        server = "http://rest.ensembl.org"

                        ext = "/info/assembly/{}?".format(msg_split[1])

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        info = r.json()

                        karyotype = info['karyotype']
                        with open("karyotype_limit.html", "r") as f:
                            contents = f.read()
                            var = ''
                            for i in karyotype:
                                var += i + ' '

                            sentence = 'The karyotype of ' + msg_split[1] + ' is: ' + var
                            contents = contents.replace('#', sentence)



            elif self.path.startswith('/chromosomeLength'):
                with open("chromosome_lenght.html", "r") as f:
                    contents = f.read()
                    f.close()
                    if self.path.startswith('/chromosomeLength?specie='):

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

                                with open("chromo_limit.html", "r") as f:
                                    contents = f.read()
                                    sentence = 'The length of the chromosome ' + chromo + ' of the species ' + msg_split2[1] + ' is: ' + str(length)
                                    contents = contents.replace('#', sentence)



            elif self.path.startswith('/geneSeq'):
                with open("gene_seq.html", "r") as f:
                    contents = f.read()
                    f.close()

                    if self.path.startswith('/geneSeq?gene='):

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
                        with open("gene_seqRes.html", "r") as f:
                            contents = f.read()
                            contents = contents.replace('#', sentence)



            elif self.path.startswith('/geneInfo'):
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

                    with open("gene_info_gene.html", "r") as f:
                            contents = f.read()
                            len= end-start
                            text= 'The start of the human gene ' + msg_split[1] + ' is: ' + str(start) + '</p></p>' + 'The end of the human gene ' + msg_split[1] + ' is: ' + str(end) + '</p></p>' + 'The lenght of the human gene ' + msg_split[1] + ' is: ' + str(len) +'</p></p>' + 'The id of the human gene ' + msg_split[1] + ' is: ' + str(id) +'</p></p>' + 'The gen ' + msg_split[1] + ' is in  the chromosome: ' + str(chromo)
                            contents = contents.replace('#', text)




            elif self.path.startswith('/geneCalc'):
                with open("gene_calc.html", "r") as f:
                    contents = f.read()
                    f.close()

                if self.path.startswith('/geneCalc?gene='):

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

                    seq = Seq(gene_sequence)

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
                    with open("gene_calResult.html", "r") as f:
                        contents = f.read()
                        contents = contents.replace('#', text)

                # Return the names of the genes located in the chromosome "chromo" from the start to end positions

            elif self.path.startswith('/geneList'):
                with open("gene_list.html", "r") as f:
                    contents = f.read()
                    f.close()

                if self.path.startswith('/geneList?chromo='):

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

                    with open("gene_listRes.html", "r") as f:
                            contents = f.read()
                            contents = contents.replace('#', sentence)



            self.send_response(200)  # -- Status line: OK!

            # Define the content-type header:

            self.send_header("Content-Type", "text/html\r\n")

            # The header is finished

            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))

            return



        except KeyError:
            f = open('error.html', 'r')
            contents = f.read()

            self.send_response(200)  # -- Status line: OK!

            # Define the content-type header:
            self.send_header("Content-Type", "text/html\r\n")

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))

        except TypeError:
            f = open('error.html', 'r')
            contents = f.read()

            self.send_response(200)  # -- Status line: OK!

            # Define the content-type header:
            self.send_header("Content-Type", "text/html\r\n")

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))








# -- Main program

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:

    print("Serving at PORT:  {}".format(PORT))



    try:

        httpd.serve_forever()

    except KeyboardInterrupt:

        httpd.server_close()



print("The server is stopped")