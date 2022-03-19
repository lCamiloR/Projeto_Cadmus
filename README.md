  # Projeto_Cadmus
  Projeto referente ao processo seletivo Cadmus.

  Para iniciar o robô é necessário se certificar que seu ambiente dispõe dos pacotes listados no requirements.txt e esteja usando Python 3.9, com isso basta executar o arquivo "main.py".
  O funcionamento da automação consiste no monitoramento do diretório "\src\SEND_MAIL\Entrance" por arquivos JSON, que devem conter as informações necessárias para sua produção:
  * Credenciais da conta de envio (Necessáriamente uma conta do Gmail);
  * Assunto do e-mail;
  * Destinatários (Lista de e-mails);
  * Corpo do e-mail;
  * Nome desejado da planilha que será enviada (Extensão .xlsx).

  Dentro do diretório \src é possível encontrar o arquivo mock_file.json, que disponibiliza toda a estrutura necessária para o arquivo de carga.
Encontrado um arquivo de carga, a automação parte para as demais etapas esperadas, de extração das vagas disponíveis na plataforma da Cadmus, criação da planilha e seu envio por e-mail. Ao final deste processo, o arquivo consumido é movido para o diretório "\src\SEND_MAIL\Sent".
