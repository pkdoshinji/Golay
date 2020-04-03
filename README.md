# Golay
Error-correcting codes for the automated correction of data transmitted across a noisy channel

The Golay codes are a family of linear error-correcting codes discovered in 1949 by the Swiss mathematician Marcel J. E. Golay. In addition to their utility in information processing, they play an important role in the mathematics of finite sporadic groups. There are four Golay codes: the binary Golay code (G23), the extended binary Golay code (G24), the ternary Golay code, and the extended ternary Golay code. The binary Golay code and the ternary Golay code are perfect codes, meaning that we can define a metric on the codespace (specifically, the Hamming metric) such that assigning a Hamming sphere of a given radius to each permissible codeword results in a partition of the codespace. It is this partition that makes error-correction possible, as any codespace vector lies within a sphere centered at one (and only one) permissible codeword.

Golay.py is a Python implementation of the Golay code. It is capable of both encoding and decoding (i.e., correcting) a data source using the extended Golay code. The encoding process maps 12-bit data words to 24-bit Golay words. Thus it doubles the number of bits transmitted. At the same time, the redundancy introduced by the size increase makes it possible to correct up to three errors per 24-bit Golay word, or one error per byte. 

So long as there are never more than 3 errors per 24-bit Golay word (or 1 error per byte), then perfect correction is possible:

<img src="example1.png" alt="example" width="850" height="400" />

However, in a realistic scenario there is unlikely to be an absolute cap on errors per 24-bit segment. A better model would assume a fixed error rate, expressed as a probability, for each transmitted bit. In this situation there may be 24-bit Golay words that exceed the 3-error correction limit of the extended Golay code. The quality of correction will then depend on the error rate. The following example illustrates correction of text transmitted over a channel with a p=0.05 error rate:

<img src="example2.png" alt="example" width="850" height="400" />
