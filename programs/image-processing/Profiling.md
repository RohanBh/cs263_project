## Performance Measurements

### Canny-Edge

* python: `19.311s, 19.443s, 20.272s, 19.591s, 20.822s`
* cython, no type info added: `19.408s, 19.396s, 19.456s, 20.039s, 19.940s`
* cython, int types and one float added, current state of `canny_edge_cython.pyx`: `19.877s, 19.798s, 20.881s, 19.688s, 19.499s`

### Marr Hildreth Edge

* Python: `8.694, 8.737, 8.832s, 8.816s, 8.909s`
* Cython, no type info added: `8.636s, 8.624s, 8.432s, 8.477s, 8.513s`
* Cython, ints and one float added (current state of `marr_cython_optim.pyx`): `7.490s, 7.655s, 7.740s, 7.693s, 7.555s`


### Evaluation Canny-Edge
Setup:
 * apply the annotations which we found:
   * try to annotate all parts of computations
   * try to annotate all variables of a for loop
   * define the funktion as cdef
   * set up numpy correctly


* cython - typed:[18.636592691997066, 18.59153202100424, 18.812104290002026, 18.7632639020012, 18.830585133997374]
* cython: [20.584371468008612, 20.54482612099673, 20.42278157999681, 20.910245947001386, 19.913509096004418]
* python: [19.67952182800218, 21.03912251201109, 20.483646750988555, 20.179445568006486, 20.266404312991654]

comments:
 * html shows, that for loops in typed version are pure C
 * types lead to some additional type conversion in typed version (maybe that's why it's not a big speedup)
 * a huge amount of the time is spent in numpy (in the measurement below roughly 70%) (we cannot get performance gains there)
   -> the improvements are heavily dependent on the type of application

```
Total time: 48.5128 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    19                                           def cannyEdge(img, sigma, th1, th2):
    20                                               """
    21                                               function finds the edges using Canny edge detection method...
    22                                               :param im:input image
    23                                               :param sigma: sigma is the std-deviation and refers to spread of gaussian
    24                                               :param th1:low threshold used to identify weak edges...
    25                                               :param th2: high threshold used to identify strong edges...
    26                                               :return:
    27                                               a binary edge image...
    28                                               """
    29
    30         1         29.0     29.0      0.0      size = int(2*(np.ceil(3*sigma))+1)
    31
    32         2        132.0     66.0      0.0      x, y = np.meshgrid(np.arange(-size/2+1, size/2+1),
    33         1          2.0      2.0      0.0                         np.arange(-size/2+1, size/2+1))
    34
    35         1          3.0      3.0      0.0      normal = 1 / (2.0 * np.pi * sigma**2)
    36
    37         2         24.0     12.0      0.0      kernel = np.exp(-(x**2+y**2) / (2.0*sigma**2)) / \
    38         1          0.0      0.0      0.0          normal  # calculating gaussian filter
    39
    40         1       4424.0   4424.0      0.0      kern_size, gauss = kernel.shape[0], np.zeros_like(img, dtype=float)
    41
    42       828        667.0      0.8      0.0      for i in range(img.shape[0]-(kern_size-1)):
    43   1044501     876674.0      0.8      1.8          for j in range(img.shape[1]-(kern_size-1)):
    44   1043674    3279292.0      3.1      6.8              window = img[i:i+kern_size, j:j+kern_size] * kernel
    45   1043674    8912813.0      8.5     18.4              gauss[i, j] = np.sum(window)
    46
    47         3         14.0      4.7      0.0      kernel, kern_size = np.array(
    48         2          2.0      1.0      0.0          [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]), 3  # edge detection
    49         3       5200.0   1733.3      0.0      gx, gy = np.zeros_like(
    50         2       2807.0   1403.5      0.0          gauss, dtype=float), np.zeros_like(gauss, dtype=float)
    51
    52       844        708.0      0.8      0.0      for i in range(gauss.shape[0]-(kern_size-1)):
    53   1078197     895563.0      0.8      1.8          for j in range(gauss.shape[1]-(kern_size-1)):
    54   1077354    1504033.0      1.4      3.1              window = gauss[i:i+kern_size, j:j+kern_size]
    55   3232062   11498061.0      3.6     23.7              gx[i, j], gy[i, j] = np.sum(
    56   2154708   13427589.0      6.2     27.7                  window * kernel.T), np.sum(window * kernel)
    57
    58         1      23133.0  23133.0      0.0      magnitude = np.sqrt(gx**2 + gy**2)
    59         1      26333.0  26333.0      0.1      theta = ((np.arctan(gy/gx))/np.pi) * 180  # radian to degree conversion
    60         1       1420.0   1420.0      0.0      nms = np.copy(magnitude)
    61
    62         1       7240.0   7240.0      0.0      theta[theta < 0] += 180
    63
    64                                               # non maximum suppression; quantization and suppression done in same step
    65       844        827.0      1.0      0.0      for i in range(theta.shape[0]-(kern_size-1)):
    66   1078197     912402.0      0.8      1.9          for j in range(theta.shape[1]-(kern_size-1)):
    67   1077354    1420601.0      1.3      2.9              if (theta[i, j] <= 22.5 or theta[i, j] > 157.5):
    68    178573     249664.0      1.4      0.5                  if(magnitude[i, j] <= magnitude[i-1, j]) and (magnitude[i, j] <= magnitude[i+1, j]):
    69     30228      31331.0      1.0      0.1                      nms[i, j] = 0
    70   1077354    1383084.0      1.3      2.9              if (theta[i, j] > 22.5 and theta[i, j] <= 67.5):
    71    215733     308334.0      1.4      0.6                  if(magnitude[i, j] <= magnitude[i-1, j-1]) and (magnitude[i, j] <= magnitude[i+1, j+1]):
    72     21943      23346.0      1.1      0.0                      nms[i, j] = 0
    73   1077354    1321601.0      1.2      2.7              if (theta[i, j] > 67.5 and theta[i, j] <= 112.5):
    74    456201     660563.0      1.4      1.4                  if(magnitude[i, j] <= magnitude[i+1, j+1]) and (magnitude[i, j] <= magnitude[i-1, j-1]):
    75     38445      41884.0      1.1      0.1                      nms[i, j] = 0
    76   1077354    1204650.0      1.1      2.5              if (theta[i, j] > 112.5 and theta[i, j] <= 157.5):
    77    193167     275797.0      1.4      0.6                  if(magnitude[i, j] <= magnitude[i+1, j-1]) and (magnitude[i, j] <= magnitude[i-1, j+1]):
    78     20211      21826.0      1.1      0.0                      nms[i, j] = 0
    79
    80         1       7217.0   7217.0      0.0      weak, strong = np.copy(nms), np.copy(nms)
    81
    82                                               # weak edges
    83         1       2384.0   2384.0      0.0      weak[weak < th1] = 0
    84         1       1357.0   1357.0      0.0      weak[weak > th2] = 0
    85
    86                                               # strong edges
    87         1       2042.0   2042.0      0.0      strong[strong < th2] = 0
    88         1       1298.0   1298.0      0.0      strong[strong > th2] = 1
    89
    90                                               # plotting multiple images
    91         1       1456.0   1456.0      0.0      fig = plt.figure()
    92         1      34778.0  34778.0      0.1      a = fig.add_subplot(2, 2, 1)
    93         1       9991.0   9991.0      0.0      imgplot = plt.imshow(gauss, cmap='gray')
    94         1        307.0    307.0      0.0      a.set_title('Gaussian')
    95         1      34070.0  34070.0      0.1      a = fig.add_subplot(2, 2, 2)
    96         1       6876.0   6876.0      0.0      imgplot = plt.imshow(magnitude, cmap='gray')
    97         1        272.0    272.0      0.0      a.set_title('Magnitude')
    98         1      34877.0  34877.0      0.1      a = fig.add_subplot(2, 2, 3)
    99         1       6527.0   6527.0      0.0      imgplot = plt.imshow(weak, cmap='gray')
   100         1        273.0    273.0      0.0      a.set_title('Weak edges')
   101         1      34382.0  34382.0      0.1      a = fig.add_subplot(2, 2, 4)
   102         1      12173.0  12173.0      0.0      imgplot = plt.imshow(255-strong, cmap='gray')
   103         1        276.0    276.0      0.0      a.set_title('Strong edges')
   104         1        128.0    128.0      0.0      plt.show()
   105
   106         1          1.0      1.0      0.0      return gauss, magnitude, weak, strong
```


### Evaluation Canny-Edge

Setup:
 * apply the annotations which we found:
   * try to annotate all parts of computations
   * try to annotate all variables of a for loop
   * define the funktion as cdef
   * set up numpy correctly

* cython - typed: [7.634226641996065, 7.510843555006431, 7.850349561005714, 7.932339325998328, 7.991159876008169]
* cython: [8.099229562998516, 8.564180334011326, 8.772020850010449, 8.93573646999721, 9.1939968069928]
* python: [8.253432225988945, 8.812853249997715, 9.2068667679996, 9.00611438199121, 8.978649369004415]

comments:
 * html shows, that for loops in typed version are pure C
 * types lead to some additional type conversion in typed version (maybe that's why it's not a big speedup)
 * a huge amount of the time is spent in numpy (in the measurement below a little less than 70%) (we cannot get performance gains there)
   -> the improvements are heavily dependent on the type of application


```
Total time: 17.4529 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    17                                           def edgesMarrHildreth(img, sigma):
    18                                               """
    19                                                       finds the edges using MarrHildreth edge detection method...
    20                                                       :param im : input image
    21                                                       :param sigma : sigma is the std-deviation and refers to the spread of gaussian
    22                                                       :return:
    23                                                       a binary edge image...
    24                                               """
    25         1         29.0     29.0      0.0      size = int(2*(np.ceil(3*sigma))+1)
    26
    27         2        136.0     68.0      0.0      x, y = np.meshgrid(np.arange(-size/2+1, size/2+1),
    28         1          3.0      3.0      0.0                         np.arange(-size/2+1, size/2+1))
    29
    30         1          3.0      3.0      0.0      normal = 1 / (2.0 * np.pi * sigma**2)
    31
    32         3         23.0      7.7      0.0      kernel = ((x**2 + y**2 - (2.0*sigma**2)) / sigma**4) * \
    33         2         14.0      7.0      0.0          np.exp(-(x**2+y**2) / (2.0*sigma**2)) / normal  # LoG filter
    34
    35         1          1.0      1.0      0.0      kern_size = kernel.shape[0]
    36         1       1675.0   1675.0      0.0      log = np.zeros_like(img, dtype=float)
    37
    38                                               # applying filter
    39       828        536.0      0.6      0.0      for i in range(img.shape[0]-(kern_size-1)):
    40   1044501     762956.0      0.7      4.4          for j in range(img.shape[1]-(kern_size-1)):
    41   1043674    3135716.0      3.0     18.0              window = img[i:i+kern_size, j:j+kern_size] * kernel
    42   1043674    8929891.0      8.6     51.2              log[i, j] = np.sum(window)
    43
    44         1       2028.0   2028.0      0.0      log = log.astype(np.int64, copy=False)
    45
    46         1       1254.0   1254.0      0.0      zero_crossing = np.zeros_like(log)
    47
    48                                               # computing zero crossing
    49       828        532.0      0.6      0.0      for i in range(log.shape[0]-(kern_size-1)):
    50   1044501     649845.0      0.6      3.7          for j in range(log.shape[1]-(kern_size-1)):
    51   1043674     965197.0      0.9      5.5              if log[i][j] == 0:
    52    414323     842259.0      2.0      4.8                  if (log[i][j-1] < 0 and log[i][j+1] > 0) or (log[i][j-1] < 0 and log[i][j+1] < 0) or (log[i-1][j] < 0 and log[i+1][j] > 0) or (log[i-1][j] > 0 and log[i+1][j] < 0):
    53      9237       8014.0      0.9      0.0                      zero_crossing[i][j] = 255
    54   1043674     989099.0      0.9      5.7              if log[i][j] < 0:
    55    509990    1063384.0      2.1      6.1                  if (log[i][j-1] > 0) or (log[i][j+1] > 0) or (log[i-1][j] > 0) or (log[i+1][j] > 0):
    56     16441      14104.0      0.9      0.1                      zero_crossing[i][j] = 255
    57
    58                                               # plotting images
    59         1       1326.0   1326.0      0.0      fig = plt.figure()
    60         1      34884.0  34884.0      0.2      a = fig.add_subplot(1, 2, 1)
    61         1       6178.0   6178.0      0.0      imgplot = plt.imshow(log, cmap='gray')
    62         1        270.0    270.0      0.0      a.set_title('Laplacian of Gaussian')
    63         1      36791.0  36791.0      0.2      a = fig.add_subplot(1, 2, 2)
    64         1       6220.0   6220.0      0.0      imgplot = plt.imshow(zero_crossing, cmap='gray')
    65         1          2.0      2.0      0.0      string = 'Zero Crossing sigma = '
    66         1          1.0      1.0      0.0      string += (str(sigma))
    67         1        268.0    268.0      0.0      a.set_title(string)
    68         1        249.0    249.0      0.0      plt.show()
    69
    70         1          1.0      1.0      0.0      return log, zero_crossing
```
