# Robo LEGO SPIKE Prime para a categoria Resgate da OBR

Este repositorio reune o codigo e os documentos do projeto de iniciacao cientifica sobre o uso de Python em um robo autonomo LEGO SPIKE Prime para a categoria Resgate da Olimpiada Brasileira de Robotica.

## Conteudo

- [codigo_robo.py](./codigo_robo.py): programa do robo, com seguimento de linha por controle proporcional, leitura de cores, desvio de obstaculos e rotinas da area de resgate.
- [documento_completo_com_imagens.docx](./documento_completo_com_imagens.docx): versao integral do relatorio, com fotografias do prototipo e descricao textual da maquina de estados.
- [trabalho_utfpr_revisado.docx](./trabalho_utfpr_revisado.docx): versao textual para submissao em sistemas que nao aceitam imagens ou tabelas.
- [robo-frente.png](./robo-frente.png) e [robo-lateral.png](./robo-lateral.png): fotografias do prototipo.

O codigo foi escrito para o ambiente LEGO SPIKE Prime e usa as bibliotecas hub, color_sensor, motor, runloop, utime e distance_sensor fornecidas pela plataforma.

## Maquina de estados

O laco principal prioriza a parada por vermelho, a confirmacao da entrada da area de resgate, o desvio de obstaculos, a marca de dois pretos e as decisoes de curva por verde. Quando nenhuma condicao especial e confirmada, o robo continua seguindo a linha. As rotinas de cada evento retornam o controle ao laco principal; a exploracao dentro da area de resgate e tratada por uma rotina propria.

## Resultados relatados

A equipe conquistou o primeiro lugar regional na area Norte do Parana e alcancou o nono lugar na etapa estadual da OBR.

## Uso

O codigo contem tempos, portas e limites ajustados para o prototipo descrito no relatorio. Eles podem precisar de calibracao para outro robo ou percurso.

## Pasta publica no Google Drive

https://drive.google.com/drive/folders/1-QyLAq80kPAi2ejt6nM-Dwg2X4G7NBcN
