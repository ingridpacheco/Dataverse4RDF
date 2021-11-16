from pyDataverse.api import DataAccessApi, NativeApi
from extract_lod_information import create_DDI_file
import subprocess as sp

if __name__ == "__main__":
    id = input('Insira o ID do arquivo: ')
    token = input('Insira o seu token: ')

    download_file_api = DataAccessApi("https://gofairbr.rnp.br", token)
    downloaded_file = download_file_api.get_datafile(id)
    file = downloaded_file.text

    api = NativeApi("https://gofairbr.rnp.br", token)
    file_metadata = api.get_datafile_metadata(id)
    current_metadata = file_metadata.json()

    print(current_metadata)

    if '.ttl' in current_metadata['label']:
        new_metadata = create_DDI_file(file)
        # print(new_metadata)
        new_metadata_file = open('new_metadata.xml', 'w')
        new_metadata_file.write(new_metadata)
        new_metadata_file.close()
        shell_command = 'curl -H "X-Dataverse-key: {0}" -X PUT https://gofairbr.rnp.br/api/edit/{1}/ --upload-file {2}'.format(token, id, 'new_metadata.xml')
        sp.run(shell_command, shell=True, stdout=sp.PIPE)
    else:
        print('Arquivo não é turtle (.ttl)')