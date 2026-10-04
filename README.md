# Robô LEGO SPIKE Prime para a categoria Resgate da OBR

Este repositório reúne o código e os documentos do projeto de iniciação científica sobre o uso de Python em um robô autônomo LEGO SPIKE Prime para a categoria Resgate da Olimpíada Brasileira de Robótica.

## Arquivos

- [codigo_robo.py](./codigo_robo.py): programa do robô, com seguimento de linha por controle proporcional, leitura de cores, desvio de obstáculos e rotinas da área de resgate.
- [versao_textual_final.docx](./versao_textual_final.docx): texto para submissão, sem imagens nem tabelas, com links para o material completo.
- [relatorio_completo_final.docx](./relatorio_completo_final.docx): relatório integral, com fotografias do protótipo e descrição textual da máquina de estados.
- [robo-frente.png](./robo-frente.png) e [robo-lateral.png](./robo-lateral.png): fotografias do protótipo.

O código foi escrito para o ambiente LEGO SPIKE Prime e usa as bibliotecas hub, color_sensor, motor, runloop, utime e distance_sensor fornecidas pela plataforma.

## Máquina de estados

O laço principal prioriza a parada por vermelho, a confirmação da entrada da área de resgate, o desvio de obstáculos, a marca de dois pretos e as decisões de curva por verde. Quando nenhuma condição especial é confirmada, o robô continua seguindo a linha. As rotinas retornam o controle ao laço principal; a exploração da área de resgate fica a cargo de uma rotina própria.

## Resultados relatados

A equipe conquistou o primeiro lugar regional na área Norte do Paraná e alcançou o nono lugar na etapa estadual da OBR.

## Uso

Os tempos, as portas e os limites do código foram ajustados para este protótipo e podem exigir calibração em outro robô ou percurso.

Pasta pública no Google Drive: https://drive.google.com/drive/folders/1-QyLAq80kPAi2ejt6nM-Dwg2X4G7NBcN
