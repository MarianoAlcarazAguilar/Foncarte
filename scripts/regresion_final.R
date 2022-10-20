setwd('/Users/mariano/Documents/topicos_negocios/foncarte/scripts')
library("lmtest")
library("lfe")
library("stargazer")
library('textreg')

data <- read.csv('../datasets/clean/dataset_final.csv', header = TRUE)
View(data)

mod <- lm(price ~ ln_height + 
                  ln_width + 
                  age + 
                  performance + 
                  year : month +
                  factor(author) +
                  factor(house) + 
                  factor(date_text) 
                  -1 , data = data) 
summary(mod)
 
# Los que voy a quitar: aquatint arches black bronze brown color gouache graphite guarro handmade ink
# laid lithographs media metal mixed mounted nylon pastel patina plexiglass print rice watercolor wove
# crayon pencil printed silver plexiglas
 
fe_mod <- felm(ln_precio ~ ln_height + ln_width + age + age_2 + age_3 + age_4 + performance 
                + acrylic 
                + board + canvas + cardboard 
                + charcoal + colors + colours + down + etching 
                + gelatin
                + lithograph + masonite 
                + mixografía + mixograph + oil + painted
                + panel + paper
                + rods + sand + screenprint
                + silkscreen + tempera + wood | author + house + year + month | 0 | 0 , data = data)
summary(fe_mod)

stargazer(fe_mod, type = 'html', out = 'regresion.html')
