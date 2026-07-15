from app.application.application_runner import ApplicationRunner
from app.application.application_statistics import ApplicationStatistics
from app.application.application_analyzer import ApplicationAnalyzer
from app.application.application_table import ApplicationTable

#
# URL de teste
#

url = "https://globo.com"

#
# Executa 5 coletas
#

resultados = ApplicationRunner().run(

    url,

    execucoes=5

)

#
# Utiliza a última execução apenas para exibição
#

resultado = resultados[-1]

#
# Estatísticas
#

estatisticas = ApplicationStatistics().calculate(

    resultados

)

#
# Análise
#

responsabilidade, conclusoes = ApplicationAnalyzer().analyze(

    resultado,

    estatisticas

)

#
# Exibição
#

ApplicationTable().show(

    resultado,

    responsabilidade,

    conclusoes,

    estatisticas

)