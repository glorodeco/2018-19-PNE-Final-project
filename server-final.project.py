import http.server
import socketserver
import termcolor
import requests, sys

PORT = 8000





class TestHandler(http.server.BaseHTTPRequestHandler):



    def do_GET(self):



        # -- Printing the request line

        reqpath = self.path

        termcolor.cprint(reqpath, 'blue')

        try:

            if reqpath == '/main_page' or reqpath == '/':

                with open("main_page.html", "r") as f:
                    contents = f.read()
                    f.close()

            elif self.path.startswith('/list_species'):
                with open("list_species.html", "r") as f:
                    contents = f.read()
                    f.close()

                    if self.path.startswith('/list_species?limit='):

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



            elif self.path.startswith('/chromosome_lenght'):
                with open("chromosome_lenght.html", "r") as f:
                    contents = f.read()
                    f.close()
                    if self.path.startswith('/chromosome_length?species='):

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

                            with open("species_limit.html", "r") as f:
                                contents = f.read()
                                sentence = 'The length of the chromosome ' + chromo + ' is: ' ' from the species ' + msg_split2[1] + ' is ' + str(length)
                                contents = contents.replace('#', sentence)



            elif self.path.startswith('/gene_seq'):
                with open("gene_seq.html", "r") as f:
                    contents = f.read()
                    f.close()

                    if self.path.startswith('/gene_seq?gene='):

                        msg_split = self.path.split('=')

                        server = "http://rest.ensembl.org"

                        ext = "/lookup/symbol/homo_sapiens/{}?".format(msg_split[1])

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        info = r.json()

                        if msg_split[1] == info['display_name']:
                            msg_split[1] = info['id']

                        server = "http://rest.ensembl.org"

                        ext = "/sequence/id/{}?".format(msg_split[1])

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        info = r.json()

                        gene_sequence = info['seq']

                        sentence = 'The sequence of the human gene ' + msg_split[1] + ' is ' + gene_sequence
                        with open("gene_seqRes.html", "r") as f:
                            contents = f.read()
                            contents = contents.replace('#', sentence)



            elif self.path.startswith('/gene_info'):
                with open("gene_info.html", "r") as f:
                    contents = f.read()
                    f.close()
                if self.path.startswith('/gene_info?gene='):

                    msg_split = self.path.split('=')

                    server = "http://rest.ensembl.org"

                    ext = "/lookup/symbol/homo_sapiens/{}?".format(msg_split[1])

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    info = r.json()

                    if msg_split[1] == info['display_name']:
                        msg_split[1] = info['id']

                    server = "http://rest.ensembl.org"

                    ext = "/lookup/id/{}?".format(msg_split[1])

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    info2 = r.json()

                    start = info2['start']

                    end = info2['end']

                    id = info2['id']

                    chromo = info2['seq_region_name']

                    with open("gene_info_gene.html", "r") as f:
                            contents = f.read()
                            text= 'The start of the human gene ' + msg_split[1] + ' is ' + str(start) + '</p></p>' + 'The end of the human gene ' + msg_split[1] + ' is ' + str(end) + '</p></p>' + 'The id of the human gene ' + msg_split[1] + ' is ' + str(id) +'</p></p>' + 'The chromosome of the human gene ' + msg_split[1] + ' is ' + str(chromo)
                            contents = contents.replace('#', text)

            self.send_response(200)  # -- Status line: OK!

            # Define the content-type header:

            self.send_header("Content-Type", "text/html\r\n")

            # The header is finished

            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))

            return


        except KeyError:
            f = open("error.html", 'r')

            contents = f.read()
            self.send_response(200)

            self.send_header('Content-Type', 'text/html')

            self.send_header('Content-Length', len(str.encode(contents)))

            self.end_headers()





        # -- Sending the body of the response message

        #self.wfile.write(str.encode(contents))



        #return





# -- Main program

with socketserver.TCPServer(("", PORT), TestHandler) as httpd:

    print("Serving at PORT:  {}".format(PORT))



    try:

        httpd.serve_forever()

    except KeyboardInterrupt:

        httpd.server_close()



print("The server is stopped")