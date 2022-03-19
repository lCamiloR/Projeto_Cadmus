# Projeto_Cadmus
Projeto referente ao processo seletivo Cadmus.

O robô consiste no monitoramento \SEND_MAIL\Entrance por arquivos .json que devem conter as informações necessárias para sua produção:
  * Credencias da conta de envio (Necessáriamente um conta do Google)
  * Assunto do e-mail
  * Destinatário
  * Corpo do e-mail
  * Nome desejado da planilha que será enviada. (Extensão .xlsx)

Dentro do diretório \src é possível encontrar o arquivo mock_file.json, que disponibiliza toda a estrutura necessária para o arquivo de carga.
Encontado um arquivo de carga, a automação parte para as demais etapas esperadas de extração das vagas disponíveis na plataforma da Cadmus, criação da planilha e seu envio por e-mail. Ao final deste processo, o arquivo consumido é movido para o diretório \SEND_MAIL\Sent.
