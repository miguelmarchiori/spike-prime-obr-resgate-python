# Robo LEGO SPIKE Prime para a categoria Resgate da OBR

Este repositorio reune o codigo e os documentos do projeto de iniciacao cientifica sobre o uso de Python em um robo autonomo LEGO SPIKE Prime para a categoria Resgate da Olimpiada Brasileira de Robotica.

## Arquivos

- [codigo_robo.py](./codigo_robo.py): programa do robo, com seguimento de linha por controle proporcional, leitura de cores, desvio de obstaculos e rotinas da area de resgate.
- [versao_textual_com_links.docx](./versao_textual_com_links.docx): texto para submissao, sem imagens nem tabelas, com links para o material completo.
- [relatorio_completo_com_fotos.docx](./relatorio_completo_com_fotos.docx): relatorio integral, com fotografias do prototipo e detalhamento textual da maquina de estados.
- [robo-frente.png](./robo-frente.png) e [robo-lateral.png](./robo-lateral.png): fotografias do prototipo.

O codigo foi escrito para o ambiente LEGO SPIKE Prime e usa as bibliotecas hub, color_sensor, motor, runloop, utime e distance_sensor da plataforma.

## Maquina de estados

O laco principal prioriza a parada por vermelho, a confirmacao da entrada da area de resgate, o desvio de obstaculos, a marca de dois pretos e as decisoes de curva por verde. Quando nenhuma condicao especial e confirmada, o robo continua seguindo a linha. As rotinas retornam o controle ao laco principal; a exploracao da area de resgate fica a cargo de uma rotina propria.

## Resultados relatados

A equipe conquistou o primeiro lugar regional na area Norte do Parana e alcancou o nono lugar na etapa estadual da OBR.

## Uso

Os tempos, as portas e os limites do codigo foram ajustados para este prototipo e podem exigir calibracao em outro robô ou percurso.

Pasta publica no Google Drive: https://drive.google.com/drive/folders/1-QyLAq80kPAi2ejt6nM-Dwg2X4G7NBcN
