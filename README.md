# Robô LEGO SPIKE Prime para a categoria Resgate da OBR

Este repositório reúne o código e os documentos do projeto de iniciação científica sobre o uso de Python em um robô autônomo LEGO SPIKE Prime para a categoria Resgate da Olimpíada Brasileira de Robótica.

## Conteúdo

- `codigo_robo.py`: programa Python do robô, com seguimento de linha por controle proporcional, leitura de cores, desvio de obstáculos e rotinas da área de resgate.
- `documento_completo_com_imagens.docx`: versão integral do relatório, com fotografias do protótipo e descrição textual da máquina de estados.
- `trabalho_utfpr_revisado.docx`: versão textual para submissão em sistemas que não aceitam imagens ou tabelas.
- `robo-frente.png` e `robo-lateral.png`: fotografias do protótipo.

O código foi escrito para o ambiente LEGO SPIKE Prime e usa as bibliotecas `hub`, `color_sensor`, `motor`, `runloop`, `utime` e `distance_sensor` fornecidas pela plataforma.

## Máquina de estados

O laço principal prioriza a parada por vermelho, a confirmação da entrada da área de resgate, o desvio de obstáculos, a marca de dois pretos e as decisões de curva por verde. Quando nenhuma condição especial é confirmada, o robô continua seguindo a linha. As rotinas de cada evento retornam o controle ao laço principal; a exploração dentro da área de resgate é tratada por uma rotina própria.

## Resultados relatados

A equipe conquistou o primeiro lugar regional na área Norte do Paraná e alcançou o nono lugar na etapa estadual da OBR.

## Uso

O código contém tempos, portas e limites ajustados para o protótipo descrito no relatório. Eles podem precisar de calibração para outro robô ou percurso.
