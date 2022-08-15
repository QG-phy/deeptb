# define the integrals formula.
import torch as th
from abc import ABC, abstractmethod

class BaseSK(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def skhij(self, **kwargs):
        '''This is a wrap function for a self-defined formula of sk integrals. one can easily modify it into whatever form they want.
        
        Returns
        -------
            The function defined by mode is called to cal skhij and returned.
        
        '''
        pass

    def skhij(self, mode='varTang96', **kwargs):
        '''This is a wrap function for a self-defined formula of sk integrals. one can easily modify it into whatever form they want.
        
        Returns
        -------
            The function defined by mode is called to cal skhij and returned.
        
        '''

        if mode == 'varTang96':
            return self.varTang96(**kwargs)
        else:
            raise ValueError('No such formula')


    def varTang96(self, alpha1, alpha2, alpha3, alpha4, rij, **kwargs):
        '''> This function calculates the value of the variational form of Tang et al 1996. without the
        environment dependent

                $$ h(rij) = \alpha_1 * (rij)^(-\alpha_2) * exp(-\alpha_3 * (rij)^(\alpha_4))$$
        '''

        hij = alpha1 * (rij**(-alpha2)) * th.exp(-alpha3 * (rij**alpha4))

        return hij    

class SKFormula(BaseSK):

    def __init__(self,mode='varTang96') -> None: 
        # one can modify this by add his own formula with the name mode to deifine num of pars.
        if mode == 'varTang96':
            self.mode = mode
            self.num_paras = 4
        else:
            raise ValueError('No such formula')
        

    def skhij(self, **kwargs):
        '''This is a wrap function for a self-defined formula of sk integrals. one can easily modify it into whatever form they want.
        
        Returns
        -------
            The function defined by mode is called to cal skhij and returned.
        
        '''

        if self.mode == 'varTang96':
            return self.varTang96(**kwargs)
        else:
            raise ValueError('No such formula')


    def varTang96(self, paraArray, rij, **kwargs):
        """> This function calculates the value of the variational form of Tang et al 1996. without the
        environment dependent

                $$ h(rij) = \alpha_1 * (rij)^(-\alpha_2) * exp(-\alpha_3 * (rij)^(\alpha_4))$$
        """

        assert len(paraArray.shape) in {2, 1}, 'paraArray should be a 2d tensor or 1d tensor'
        paraArray = paraArray.view(-1, self.num_paras)
        alpha1, alpha2, alpha3, alpha4 = paraArray[:, 0], paraArray[:, 1], paraArray[:, 2], paraArray[:, 3]

        return alpha1 * rij**(-alpha2) * th.exp(-alpha3 * rij**alpha4)    

