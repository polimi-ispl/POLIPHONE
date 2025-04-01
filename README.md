# POLIPHONE: A Dataset for Smartphone Model Identification from Audio Recordings

This repository contains the implementation accompanying the paper *"POLIPHONE: A Dataset for Smartphone Model Identification from Audio Recordings."* 
The toolkit enables impulse response analysis for smartphone audio characterization.  

## Overview

The repository provides MATLAB and Python implementations for:

- **Sweep Signal Generation**: Tools for creating and inverting logarithmic sine sweeps used for excitation
- **Impulse Response Extraction**: Methods to estimate linear and non-linear impulse responses from recorded sweeps
- **Audio Characterization**: Algorithms for reverberation time estimation and device fingerprinting
- **Analysis Utilities**: Signal processing pipelines for comparing recorded signals with reference audio

The MATLAB implementation focuses on core signal processing routines, while the Python version includes additional analysis tools for practical device evaluation.


## Usage - Basic Workflow

1. Generate excitation signals (sweeps or noise)
2. Record device responses to these signals
3. Extract impulse responses
4. Analyze device characteristics (T60, non-linearities, etc.)


## Citation

If you use this code in your research, please cite the following paper:

**Salvi, D., Leonzio, D.U., Giganti, A., Eutizi, C., Mandelli, S., Bestagini, P., & Tubaro, S. (2025).** *POLIPHONE: A Dataset for Smartphone Model Identification from Audio Recordings.* In *IEEE Access*.

```
@ARTICLE{10902157,
  author={Salvi, Davide and Leonzio, Daniele Ugo and Giganti, Antonio and Eutizi, Claudio and Mandelli, Sara and Bestagini, Paolo and Tubaro, Stefano},
  journal={IEEE Access}, 
  title={POLIPHONE: A Dataset for Smartphone Model Identification from Audio Recordings}, 
  year={2025},
  doi={10.1109/ACCESS.2025.3545152}
}
```

## License

The code is provided for non-commercial research purposes only. For commercial use, please contact the authors.

## Contact

For any inquiries or collaboration requests, please contact:

- **Davide Salvi**: davide.salvi@polimi.it
- **Leonzio Daniele Ugo**: danieleugo.leonzio@polimi.it
- **Antonio Giganti**: antonio.giganti@polimi.it
- **Claudio Eutizi**: claudio.eutizi@mail.polimi.it
- **Sara Mandelli**: sara.mandelli@polimi.it
- **Paolo Bestagini**: paolo.bestagini@polimi.it
- **Stefano Tubaro**: stefano.tubaro@polimi.it
