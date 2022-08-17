import pdb
import unittest
import os, sys

sys.path.extend(['.', '..', '../..'])
from rc_pick import RCPick
from rc_parser.rc_lex import RCLexer
from rc_parser.rc_parse import RCParser, RCParserError
import common.objects as obj
from common.utilities.bump import Bump

class TestRCParser(unittest.TestCase):

    def setUp(self):
        self.collection = RCPick.manage()
        self.selection = [
            'MITCHELL: Finally (7.23) R. Mitchell / K.Barron.',
            'TRADICIONAL: Lord you made us human (3.41) D.Washington.',
            "PARKER: Now's the time (8.49) M. Davis.",
            'PRAETORIUS: Magnificat per omnes versus super ut re mi fa sol la (18.55). Coro Balthasar Neumann, EnsembleBalthasar Neumann. Dir.: P. Heras-Casado. Ach mein Herre, straf mich doch nicht (10.36). La Capella Ducale,Musica Fiata de Colonia. Dir.: R. Wilson.',
            'STRAVINSKY: Concierto para orquesta de cámara en Mi bemol mayor “Dumbarton Oaks” (arr. para dos p.) (14.11).H. Bugallo (p.), A. Williams (p.), Dúo de piano Bugallo-Williams. Le baiser de la fée (selec.) (arr. para vc. y p.)(Escena 3. Adagio, Variación y coda) (7.32). M. Rostropovich (vc.), A. Dedyukhin (p.). Suite para pequeña orquestanº 1 (arr. de los nº 1 al 4 de 5 Piezas fáciles para piano a 4 manos) (Balalaika, grabación del ensayo) (6.01). Orq. dela Radiotelevisión de la Svizzera Italiana. Dir.: I. Stravinsky.',
            'HARTMANN: Obertura Un viaje nórdico, Op. 25 (13.06). Obertura de concierto Una cacería de otoño, Op. 63b(9.05). Orq. Sinf. Sonderjyllands. Dir.: J. P. Wallez.Música en familia: La familia Hartmann.',
            'HARTMANN: Hakon Jarl, Op. 40 (9.01). Hakon Jarl, Op. 40 (19.01). Orq.Sinf. Sonderjyllands. Dir.: J. P. Wallez.Ediciones y reediciones: Cameristas infrecuentes.',
            'BRAGA SANTOS: Pieza para flauta y piano (2.38). Nocturno, Op.1 y Aria, Op. 2 (12.50). Aria a tres con variaciones, Op. 62 (9.07). N. I. Cruz (fl.), A. Saiote (clar.), L. Pacheco (vl.), L.Braga (vla.), I. Lima (vc.) y O. Prats (p.).',
            'FARKAS: Nocturno para trío de cuerdas (11.08). Tres piezas para flauta,cello y clave (6.17). Prélude et Chaconne égarée para cuarteto de cuerdas (5.18). K. Baráti y E. L. Bedö (vl.), P.Bársony (vla.), M. Perényi (vc.), V. Oross (fl.) y M. Spányi (clv.).',
            'GADE: Capricho para violín y orquesta en La menor (9.14). Concierto para violínnº 2 en Fa mayor, Op. 10 (29.30). C. Astrand (vl.), Orq. Sinf. Sonderjyllands. Dir.: I. Brown.Ediciones y reediciones: Volumen 5.',
            'SWEELINCK/PRAETORIUS: Pavana hispánica (2.51). M. Gnuebder (espineta), EnsembleRicercare fur Alte Musik Zurich. Da Pacem Domine in Diebus Nostris (8.44). G. Leonhardt (org.).',
        ]
        self.lexer = RCLexer()
        self.parser = RCParser()
        self.bump = Bump()

#   def test_parser_full(self):
#       for c in self.collection:
#           fn = os.path.basename(c.filename)
#           for cl, date, time in c.find_composer_lines():
#               for work in RCPick.separate_composers(cl):
#                   try:
#                       rec = self.parser.parse(self.lexer.tokenize(work))
#                       # for rec in self.parser.parse(self.lexer.tokenize(work)):
#                       # for rec in recs:
#                       self.assertTrue(type(rec) is obj.Recording)
#                       self.assertTrue(rec.composer)
#                       self.bump.bump()
#                   except RCParserError as rcpe:
#                       print("%s:%s:\n\t%s" % (fn, work, rcpe), file=sys.stderr)

#           c.pdf.close()

    def test_parser_selected(self):
        for line in self.selection:
            rec = self.parser.safe_parse(self.lexer.tokenize(line))
            # pdb.set_trace()
            self.assertTrue(type(rec) is obj.Recording, line)
            self.assertTrue(rec.composer, line)
            print(rec.__dict__)
            self.bump.bump()

if __name__ == '__main__':
  unittest.main()
