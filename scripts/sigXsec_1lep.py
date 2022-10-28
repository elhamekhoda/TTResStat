#!/usr/bin/env python

signalList= [
              'zprime400',
              'zprime500',
              'zprime750',
              'zprime1000',
              'zprime1250',
              'zprime1500',
              'zprime1750',
              'zprime2000',
              #'zprime2250',
              'zprime2500',
              #'zprime2750',
              'zprime3000',
              'zprime4000',
              'zprime5000',
              #'zprime6000'
              ]

mass= {
    'zprime400' :0.40,
    'zprime500' :0.50,
    'zprime750' :0.75,
    'zprime1000': 1.0, 
    'zprime1250': 1.25,
    'zprime1500': 1.5,
    'zprime1750': 1.75,
    'zprime2000': 2.0,
    'zprime2250': 2.25,
    'zprime2500': 2.5,
    'zprime2750': 2.75,
    'zprime3000': 3,
    'zprime4000': 4,
    'zprime5000': 5,
    'zprime6000': 6
    }

xs = {
  'zprime400' : 70.2764206532*1.3,
  'zprime500' : 40.1252717501*1.3,
  'zprime750' : 10.7025592052*1.3,
  'zprime1000': 3.69900238076*1.3,
  'zprime1250': 1.50806798183*1.3,
  'zprime1500': 0.684451508485*1.3,
  'zprime1750': 0.334388285018*1.3,
  'zprime2000': 0.172299333764*1.3,
  'zprime2250': 0.0923739492669*1.3,
  'zprime2500': 0.0510543839336*1.3,
  'zprime2750': 0.0289022800871*1.3,
  'zprime3000': 0.0166807659717*1.3,
  'zprime4000': 0.00212729713173*1.3,
  'zprime5000': 0.000330792326516*1.3,
  'zprime6000': 7.17103e-5*1.3
  }


# #Graviton
# signalList = [
#               'grav400',
#               'grav500',
#               'grav750',
#               'grav1000',
#               'grav2000',
#               # 'grav3000'
#               ]

# mass = {
#         'grav400':0.4,
#         'grav500':0.5,
#         'grav750':0.75,
#         'grav1000':1,
#         'grav2000':2,
#         'grav3000':3
#         }

# xs = {
#        'grav400': 7.19,
#        'grav500': 5.84,
#        'grav750': 1.18,
#        'grav1000': 0.289,
#        'grav2000': 0.00498,
#        'grav3000': 0.000248
#        }


# signalList = [
#             'gluon500',
#             'gluon1000',
#             'gluon1500',
#             'gluon2000',
#             'gluon2500',
#             'gluon3000',
#             'gluon3500',
#             'gluon4000',
#             'gluon4500',
#             'gluon5000'
#             ]
# mass = {
#          'gluon500': 0.5,
#          'gluon1000': 1.0,
#          'gluon1500': 1.5,
#          'gluon2000': 2.0,
#          'gluon2500': 2.5,
#          'gluon3000': 3.0,
#          'gluon3500': 3.5,
#          'gluon4000': 4.0,
#          'gluon4500': 4.5,
#          'gluon5000': 5.0
#          }


# xs = {
#       'gluon500': 91.946244,
#       'gluon1000': 8.05651215,
#       'gluon1500': 1.54465083,
#       'gluon2000': 0.4266680898,
#       'gluon2500': 0.1494520676,
#       'gluon3000': 0.0622959605,
#       'gluon3500': 0.02966500351,
#       'gluon4000': 0.01581725076,
#       'gluon4500': 0.00925413031,
#       'gluon5000': 0.00581167335,
#       }

signalListMorphed= [ 
              'zprime1750',
              'zprime1875',
              'zprime2000',
              'zprime2125',
              'zprime2250',
              'zprime2375',
              'zprime2500',
              'zprime2625',
              'zprime2750',
              'zprime2875',
              'zprime3000',
              'zprime3250',
              'zprime3500',
              'zprime3750',
              'zprime4000',
              'zprime4250',
              'zprime4500',
              'zprime4750',
              'zprime5000',
              #'zprime5250',
              #'zprime5500',
              #'zprime5750',
              #'zprime6000'
              ]

massMorphed= {
    'zprime1750': 1.75,
    'zprime1875': 1.875,
    'zprime2000': 2.0,
    'zprime2125': 2.125,
    'zprime2250': 2.25,
    'zprime2375': 2.375,
    'zprime2500': 2.5,
    'zprime2625': 2.625,
    'zprime2750': 2.75,
    'zprime2875': 2.875,
    'zprime3000': 3.,
    'zprime3250': 3.25,
    'zprime3500': 3.5,
    'zprime3750': 3.75,
    'zprime4000': 4.,
    'zprime4250': 4.25,
    'zprime4500': 4.5,
    'zprime4750': 4.75,
    'zprime5000': 5.,
    'zprime5250': 5.25,
    'zprime5500': 5.50,
    'zprime5750': 5.75,
    'zprime6000': 6.00
    }

xsMorphed = {
  'zprime1750': 0.334388   *1.3,
  'zprime1875': 0.238696   *1.3,
  'zprime2000': 0.172299   *1.3,
  'zprime2125': 0.125612   *1.3,
  'zprime2250': 0.092374   *1.3,
  'zprime2375': 0.0684446  *1.3,
  'zprime2500': 0.051054   *1.3,
  'zprime2625': 0.0383094  *1.3,
  'zprime2750': 0.028902   *1.3,
  'zprime2875': 0.0219111  *1.3,
  'zprime3000': 0.016681   *1.3,
  'zprime3250': 0.00977134 *1.3,
  'zprime3500': 0.00580195 *1.3,
  'zprime3750': 0.00349072 *1.3,
  'zprime4000': 0.0021272  *1.3,
  'zprime4250': 0.00131246 *1.3,
  'zprime4500': 0.000819562*1.3,
  'zprime4750': 0.000517757*1.3,
  'zprime5000': 0.00033079 *1.3,
  #'zprime5250': 0.000252282*1.3,
  #'zprime5500': 0.000173775*1.3,
  #'zprime5750': 9.52680e-05*1.3,
  #'zprime6000': 0.000012384*1.3534236117*1.3
  'zprime5250': 0.00021712 *1.3,
  'zprime5500': 0.000145591*1.3,
  'zprime5750': 0.000100914*1.3,
  'zprime6000': 7.17103e-5*1.3
}

xsMorphed_TC2 = {
  'zprime1750': 0.334388   *1.3,
  'zprime1875': 0.238696   *1.3,
  'zprime2000': 0.172299   *1.3,
  'zprime2125': 0.125612   *1.3,
  'zprime2250': 0.092374   *1.3,
  'zprime2375': 0.0684446  *1.3,
  'zprime2500': 0.051054   *1.3,
  'zprime2625': 0.0383094  *1.3,
  'zprime2750': 0.028902   *1.3,
  'zprime2875': 0.0219111  *1.3,
  'zprime3000': 0.016681   *1.3,
  'zprime3250': 0.00977134 *1.3,
  'zprime3500': 0.00580195 *1.3,
  'zprime3750': 0.00349072 *1.3,
  'zprime4000': 0.0021272  *1.3,
  'zprime4250': 0.00131246 *1.3,
  'zprime4500': 0.000819562*1.3,
  'zprime4750': 0.000517757*1.3,
  'zprime5000': 0.00033079 *1.3,
  'zprime5250': 0.00021712 *1.3,
  'zprime5500': 0.000145591*1.3,
  'zprime5750': 0.000100914*1.3,
  'zprime6000': 7.17103e-5*1.3
}

# Z' TC2: 3% width cross section
xs_TC2_3p = {
  'zprime1750': 1.10360e+00,
  'zprime2000': 5.64587e-01,
  'zprime2250': 3.01085e-01,
  'zprime2500': 1.66007e-01,
  'zprime2750': 9.40538e-02,
  'zprime3000': 5.45784e-02,
  'zprime3250': 3.23203e-02,
  'zprime3500': 1.95239e-02,
  'zprime3750': 1.20183e-02,
  'zprime4000': 7.56074e-03,
  'zprime4250': 4.85925e-03,
  'zprime4500': 3.20525e-03,
  'zprime4750': 2.17011e-03,
  'zprime5000': 1.51347e-03,
  'zprime5250': 1.08776e-03,
  'zprime5500': 8.05684e-04,
  'zprime5750': 6.14711e-04,
  'zprime6000': 4.80939e-04
}

# Z' TC2: 1% width cross section
xs_TC2_1p =   {
  'zprime1750': 3.61087e-01,
  'zprime2000': 1.83366e-01,
  'zprime2250': 9.67045e-02,
  'zprime2500': 5.27004e-02,
  'zprime2750': 2.92963e-02,
  'zprime3000': 1.66912e-02,
  'zprime3250': 9.62732e-03,
  'zprime3500': 5.63258e-03,
  'zprime3750': 3.34041e-03,
  'zprime4000': 2.00280e-03,
  'zprime4250': 1.21849e-03,
  'zprime4500': 7.51813e-04,
  'zprime4750': 4.70802e-04,
  'zprime5000': 3.02108e-04,
  'zprime5250': 1.98522e-04,
  'zprime5500': 1.34385e-04,
  'zprime5750': 9.42072e-05,
  'zprime6000': 6.85090e-05
}


zprime_list = ['zprime1750',
'zprime2000',
'zprime2250',
'zprime2500',
'zprime2750',
'zprime3000',
'zprime3250',
'zprime3500',
'zprime3750',
'zprime4000',
'zprime4250',
'zprime4500',
'zprime4750',
'zprime5000',
#'zprime5250',
#'zprime5500',
#'zprime5750',
#'zprime6000'
]

mass_list = [1.75,
2.0,
2.25,
2.5,
2.75,
3.0,
3.25,
3.5,
3.75,
4.0,
4.25,
4.5,
4.75,
5.0,
5.25,
5.5,
5.75,
6.0]


