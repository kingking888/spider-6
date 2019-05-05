#encoding=utf-8
import requests,json,re,time,datetime
import hashlib
from lxml import etree
from insert import insert
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class QuTouTiaoVideo(insert):
    def __init__(self):
        insert.__init__(self)
    def getlinkurls(self):
        """
          dict = {
                '推荐':'https://api.1sapp.com/content/getListV2?qdata=OEM5ODZDNEI0ODU3RkNCRTA1MDBCRTY4ODBGNDY2MTUuY0dGeVlXMGZaV014WldFME16VXROamMxT0MwME9USTRMVGc0T0RJdE5EaGtNVGxrTWpJd1lXUXpIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuC6sI2qVMUfhjwtbGwZuJZpPHyifvb4okXX96r2bqyFLgV26snb25e3D%2FeQ73MGeduLt%2BosE%2BWZq3cb3s4nZhhBL3Zw18DHcwG7FqqBwcbVbR1VCixVyiZ2ZmD3iyRIq%2Fuyc3s8qfze5t%2Fg2Mm%2BOxVBq21kgbNUn6GvjhGKYpEnpLoqPbsk2tH5QJlJ8FKSIJfkDRIcZKeUoSlGTKferfl04SWBLfBvGaSlj2weSmDN%2FI5Gx%2BKYUByIrGC8B5lUFVebi7JMR6iMAvpYM8ETYAPEJ8Rxr%2BTwoW77xpME%2BmySxwxxfXDnEmmjIJADbomDGhH1MY0fDDgsBhy2mxrEXv4QKynwbJ7%2FCa6W9xrARxRLYIxhmJOmfpJcvRTulZeXCUR%2BRB64byMVrxrwBTB%2BFq7xRR2DzLMm8jLPD3k3dC3yngog8n0o7X1dYrQ0R87yNCA5J8xDw2jBOsRBuI6eSuCp11Xsx%2FGutPSf3ycuxeEdtO8Ljo9%2FBgV%2BvYK%2FNFYhkhePVG10BN7pwo504xyd4MfWg%3D',
                '娱乐':'http://api.1sapp.com/content/getListV2?qdata=QTVBMURGQ0FDRDJCQzE3RENFMEU1M0YyNkQ4QjUxNTEuY0dGeVlXMGZaRGxtWmpjeVptVXROemt3TmkwMFptWTFMV0ZoWlRRdE0yVTBaalF5TlRFNE16RTBIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuH0SQKuQmrPR99JSI7nkHtUxqT4eAGMSlDcK1VEkQ0qPODbFpszp%2Bjytw3%2BiiufQAKJjB9cpM%2FZ%2FI9kZRh%2BW73NjyDDBBU954H2wO3B3AhxOlRLMNiMgKvXhq3Hj4ZSVAFGj8HwsFdCHL28Kj%2BKVtccy7uX0v4LnBbR1yBXFRcm564ZuclpW9KsgYuQeeBvQL%2Bnh6rNJkpBnUX7YnKSER17kFclpKwV17%2FnpfTodtHX2qBkR8sbnqiJm9KR7G4x9zQJNAPy2q%2Fh1%2FIZlYlW3Vu3wrxDbRhvJgV0rpje227X5k7fxD2RZV2rXkolRF5ZubQEKkJ%2BAREgdkVmW4O3QVxp%2F18HLdjXvtPNHmSWptypnLY3gHUuTX47tJ82tuxEQ2wmxVxzh1XeRgRn9LIDniLouRPf8MqRUUbTermlKvG6dhj%2FhTCeRj8fzyl6ASe5aEG8iao8wOqtorZlFznrQ38n7szHTL0uwoWdyLoGyGDen43Rc%2FaZC8YaFc2UYmvyKYus%2F%2F2gcpWXMkSxiEMVH8Y6Q%3D',
                '影视':'https://api.1sapp.com/content/getListV2?qdata=MTM2RDBFRjUxOTBEQUY2Mzc1RDM2N0ExODY3MkRGNzYuY0dGeVlXMGZNR1prTkRVd01UVXRNVGd5WmkwME9UUXpMV0k0WVdZdE56ZzBNemxrT0RWa05EWXpIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuCsbfahNLECPqCG4P%2F%2FbQUvHgdzZ9kPJIajyMepXmeRqn8uCY1uEBCS%2FY2JWDArJ9P0R3r2NLvIEvR%2BNIi0RRgNy02O47z37YTcoDUt1cQQunSkrGyRDAGOShmhrhNI6P7PWpcZx153TtNaWgHw%2BEEulHpocG70V79av9JAW%2BTATeUtbWy5A8qIY57kfCs%2Fg8Rh0Vo2V2p0yuNHawLCzoy5W7JgLdwqhbxoK3AEqxTPa0btBsdjZ7I3iWtCjprz2k9K0NSQKwttoTYDnGUuvrwc%2FhBItXDR8V1PthDXOF29M6MWpMkYdx2CAyWX3zEsUb0q6Dn9YVm3xm6Sp657eGVdlKSKOqbD1NqbFH9xDuqfkBcB7V1pQAsTwPmzKXAfa8qEkNyVyH6VuWgohK7mEIHNM912fgmZ4%2FCZJw%2F0mZD50kmZ9PgqW%2FOeNUhdD84o7Ilb4aAcMLGTiNSPx1Sm83lrXoa64H0no%2BQ3GzYZVHV9G%2FpO8xC%2FxmjdeJ4hiHlBsqqUExTb3lqLMupbL3tMHNfTk%3D',
                '汽车':'https://api.1sapp.com/content/getListV2?qdata=MjFDNDM4RUMyOTQxMDdBNjE5MzZDOEIzRkRCQUY0OUEuY0dGeVlXMGZOV1ExWkRRMllUZ3RaV0psTmkwME4yWXhMVGxsWXpRdE5XSTFObU5rTlRaak1USmpIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuFv79cIPSRHGlYguUrPyb3j50grWMcRDl8zlgKwS6yLBCzALlCtHIanl52foD9zw9n4r%2FORuNxfjWcl4gkG0tAlD9B3%2BGeDuldv707HZkpQbUCbKbBpdqunqXakA8eZ38DJtV4hV8cULnZHp6%2BPinpshJbzvgfvcOIk5D0GWMohbDFDO4EKC1%2Fs%2BKOALMBEGSfKXrl4dG%2BiOE0xORbtKk%2BD3ZAxsWfS%2Bmy4IE1MKOtiC7KoxyJyC2GNLXNR9xZt7SCkt3V6a54gR%2B7McizTtgC91jqJG7LKhC4WA7zsAeTpDKkzNZfc7tCK9gFit5tvN5U00d5Ti5buWCW4%2FHIx0bf0%2BWOoYbRrnmXe8PCrIOv7%2FdDBpJ851P%2FSIyQ6wqjjWfjbr0mQXcOjmWXtY5Q3LtDdz7YOrJLRh%2B8IbB7%2BDyN1KFIrufGLB%2BB2uc%2FhRbZKdhUpCY48c8uxhA2PkbahNEKktsaVdo11blNGHZVOSwiHV7CWkeoUaNnHnwIGYFF7IKPgQ1j9viV7TQ0QvpeMKBeww%3D',
                '美食':'https://api.1sapp.com/content/getListV2?qdata=NTVBRjFBNTcxQzlBMEFGQTVFRTIwMkY5RkUwRkQ4NzkuY0dGeVlXMGZZemN6WWpjek1Ua3RObUkxTVMwMFpqSTFMVGxpTVRFdE5qYzFaRFUzTm1RMFpqSmhIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuCjkxz%2Fy6by57Ifr7lHaIAj9tSWMBCB7sAQeLj69AW9GcY%2Btg5MiON5aaYumGooK%2BtKBdo%2FNFOv42e4p%2Fl%2Fvr8vhtmkQu85i5qzFMZt2WfGVir8t3BD4fWht5Dys0dXQYmHbc78s%2BdJF46TgfkezKaSop2QBbWzW08xpwIETg7We5Viw%2FMKIr6QXaBr92Z4EifCPWN241%2FK7j166HTk5Ut4gICTQTrWceaOXFXNa9tRFDeVlwFw2N3FF7lZQjdHTksmJF%2FcnqMVAVffqwPAJJMwew%2BL0NKvZCMvkzyTjQoqnhN6bXaw4J6o5Wk%2BlyfmlrOP1drvphUvRWUAyoU9unwlxxkLVrYpSKkFd4oqjo%2Bl2F3hdnp2K%2Bf7aNN%2Frw9g14b3sHpxQMInOn4NbUctC4i4umBK%2F9UuK2XHHtDwVVxmY9ISAc5mmYkI6pdk%2F1%2Fu9znGPIHFKtjCJboDL9cxlmarQRntZPtIXxBxOMijuxOl67DP%2F9EBX5KPt4EOpWSdok1qKGto%2BKiwIs1N6ls1fq3fQ%3D',
                '生活':'https://api.1sapp.com/content/getListV2?qdata=MDM5QTQwOEQ4QjNGNkY5RUEyNTQ5REFBMDYzMDY0NzQuY0dGeVlXMGZNR1kwWVdaak9UWXRNV05rWVMwME1qSTVMV0ZoTjJVdE5EZ3dOV0ptWXpFNFl6SmxIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuZJTApUpy22hlkzET1DnTcEdZ1BWEka7Gu4ZFGEOLEJe%2F0lpAt8uQg%2BYSJKegqrNWpOZpX7GBmWqg7fSEFMUPOK8QrvFCKtyvKzN989mNNsb9nD1yTd4CEHkwMtbD6UV5xerIdWDvvcKsRkQbdSk28DLXsueOfCnwqpv21wK3FM%2FsYNoSTPkvHohBPLmSrlCm8SscMnjmlDljfuZVCjPX4ALddQLrigRBr6pB3qqSn%2FA3V%2BBBeTf8KYp0hNeFv6A1KgmepfRMkiSUiyk%2Bm6x2qUNm8YfRDSuEUjyV343IPuZ08KjZxVmuOaBYItKRmeXt4E1p2pFe1YEv9CxD4JQ8QZmelfA7lNwwJbnDAeXBW4kMmsI1uJhasKQl5LcRhLKYKlKWp2HFbTzWzGmBr0zjG7OLyx8JBt149I5SKbA9ZAvkoJof33gOnngblv2cMLfsQtUIlhIceZvaYpPbbQ8hPNa%2FuRK0NikKIllhkeaIqnsKtkbzPvzpV9cwgm7BCy4UzO2qFr28kb3Mc7YByqPs6gg%3D',
                '科技':'https://api.1sapp.com/content/getListV2?qdata=MjRCQkE4Q0QwNkMyNUQzMjE5NjRGMDIzMkEzNkQ3MkUuY0dGeVlXMGZORFpoWVRZeE9HWXRNREU0WlMwME9XRmpMVGd6WmpZdE1qRmtZV0l3WVRGbE1XVTFIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuSyYF0JHLkRX8N2vrRr9KGnFbwixHZBBYTlwNKBiDSWGovifKFNIlNfuOf32iOO0EN5gsAbT6o%2BvgBtZlL%2FKqs7My3WgfZPiFfhTx3svPlg8c8qqecndZoiZGYkXz%2BP3L%2BzhjrRfBZRBZf8b8HO0JujjBRtdTkepyAUk%2BYNqJdysWLXJyJU66qj5zTUv4gX3XfGrVQoGo4vi5wM356Ff1reOQxS4fHPxWn5xkwXWnw6tJBc9gXm6%2F7ujIOGfdDA7cjK5lOD1Zi3dvA8feS7cd7vvOCT8sgB4eWencJUB2GlfahY5eIXD%2FdTp3bqEmwC5eTJ%2BYKd3R0IBGGW%2BFOJvBBid7NHqvIrYSAT8XrosM4b%2FNiVgGYaOokCsHeQHSIHkkJioT%2FcH7pHTST%2Bvru%2B6rD0sOD53QvGc82B%2BOrdRne6%2BFlBlLoPFq5UFH44E04LMX%2FmFFAEk9suntaKEjWQHt6MEpTnmjB5uIHc2aTh7sZopqu0AfsVqygR%2FMhydkAGu1AutuhIb6YQP7Bv4pRy04FeU%3D',
                '秘史':'https://api.1sapp.com/content/getListV2?qdata=OEY2OTZGNjREQkQ5QkY0OEU1ODk0MEE5RUY3MjNDOTMuY0dGeVlXMGZPRGRoTnpGaVpqWXRPR0ZtWlMwMFpqYzNMV0kxWkRZdFpEUTBPR1U0TWpjMU5qbGhIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuSQoR8szVJH8yRKYV9ykWMZyQ0t8Il5OlF76KSop87bp1E8DE9YNTB5Yld2WlaEt51JWxK1eL3YyyL7DWR1ms4HjxpYJrneQS9%2FLfKMN1LQSk3zVIp8zfXnmIM0LP2PoG2Lk9I1vkvUFHkPZiKFsdZDxr6ZVtHap3gPUfgGOgInALrMb%2FuAcpPdka4q1dpNx6cTqHTY3zhxC%2FtL7bhmV0ikpkh73HA8HuzFs1Xd76HzXU5VkWkjJJzFmvLXJuldA8g5%2F2ercrsR5vEtVHgRD4llecWQnEa0Rpc1kwvKGL3DVatLoj8tucgjxFm1I788hD1soNjc5mHIsZyWWxSO%2FAHQYiH%2FxD8tZDm3vVHAPmjeH%2FLfEGZIyuztmlTh2vFGsLE9p8EEJdPeA1a8Q%2FuuzM%2Fb10f9RkJO1yJogBQ5D8CYF2SmoMb5L61P6BU3m%2FbOKdmXulOny01%2BS5Etze5xJqKV0plRm5OjuMtjKlLKEaFkh1SnRHatwwE81JG5T%2BsQfkILlqnqnwG4yEH7cJOHSZ9QM%3D',
                '旅行':'https://api.1sapp.com/content/getListV2?qdata=RjAyNUM0QTQ2RUQ4MThEODQzMDc3RkQ2NDEwRkY1NEMuY0dGeVlXMGZORGxtWlRVMFl6TXRPRGM0TmkwMFpXVTNMVGhqWmpjdFlUWmxabU14TkdRNFpqUmlIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsu%2BD4O%2FUpgrytaDeqfmC%2BB1aP8%2BO%2BpJ2bkPNaZF320f8%2B65%2BBWX62ZFSDpRZMniU%2F%2FcCokjA%2FlnjIExY8cNdVNzCPg%2FozbyQsvfuJRd8fVnheuGA%2BmlAhlxF7RPK6QOrLq1YM4kG6z%2FeIEA97%2FZECBsdhMZih82nCPzBxSjiBurTe6MHLN1sSB0PDQacsVI3%2Fc6EFRaL9s8F6QmYw87OBN9lXFduHMnAdDpPwD9ocJG1WErwsiIUL3w4jV9CSjHNyxbienJMNKeSR0lqNo3dMgekP8vPcX4%2BUtuWTXKJ5gQlkykW4TPafT5ENxn9K%2FUEzQA%2FRQ%2BqhbL8cFAjELg%2B6toJHjYLXS9cCddyxmhm7FcDkJN2%2FzH13DWuSLx2UjNgVbnP0%2BytrkF8Ufb2rJmCn7g4okQcz1bQRPjWFixmD8gcRfvAyf3E2GEBFrkvfsMtL3WIe8rszNAZFCo1jxPje%2FzXJktIrmzW69wesFp9TC7ltWv6RP0%2FNy8415Q%2BL2ht5lFk4R28k6a9ISXLj79xFMkH8%3D',
                '体育':'https://api.1sapp.com/content/getListV2?qdata=MDNDQTQwRDNCRTBGQjZDNjg0N0M5NjE2RjVDNDI3MEYuY0dGeVlXMGZObVZtTUdVeFlqZ3RaREkzTVMwMFlUWTFMVGhsWkRJdE5UTmhZV05oWTJJek1ESXpIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsu1T7MCi7BJY830Wn5eMwyErqc3jIiQ6V3gyA3XjZbvM3eabH%2FUCb1mKxTPT%2BibidCGlLjwHi2L4XHNIwoiDY6RsLmMCyoKoiAvEMTHPSkgp6PB9OfNDFRQX0%2BJEFF4btP4xzOFCy3fU8DkcrpMLrACKrWKFARNaJjY1HTDUzr4uGlbth2frzCQJ0pG8Qtgjt3lnfJqPkh78qUBz4I874nUXQFUffU7KAXlb2JIEj1U0w7dtkzz7yHwHe04VC6eGuzrDReIy7%2BNL5ZEZ8wxbKoPL%2F5VEBOu%2FxIvaimJnvM%2FEyfmxhoyV4fZWxrRzEIY%2B1QjaSNmVrqAw2OhOZVPpX%2FjUwQSw78FoyX5W%2FzZvkXM%2B9vaykAFA55u4mpun6NcPf%2Fsypc0KXzxZZs0Aftu4fhr8SoIKj%2Fq2n2Uwf5Rpxgvy1y%2FOxaoAruOHgVlmmHYqTs%2FP7Gyth4XW9QsFoJ8rKWRKTKDZdhz1gtpzFvU03b%2B9%2BVrK7JqtgqCcLgTFaZzoAfUmX%2FWgCVhPfHbMFKILhFM94%3D',
                '游戏':'https://api.1sapp.com/content/getListV2?qdata=OTk3NjQxMkIxOEIzQjkxRTZFRjEyOUI0OTI1MEFCOTYuY0dGeVlXMGZOamMyTjJJMVpUSXROelJtTnkwMFpEZzJMVGsyT1dVdE0yRmpNV0UzTkdRME5EQTVIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuYO%2FveZwtYEnFFqVsrnzR6uJvI4hwc8STTtaLBTkzZh7ks2r0Y6%2BB%2BAvo96SFBafAfzXGs2%2BpDyA7I6XfwNt48oaICKiZnHaNJcJlldrIDjQOCXC6AE%2FgSAvrCt4gXijt74gt51IsnPiVWoa8ygUEF%2FLPj%2Fi3ZKo9jmHETrhYep7fHbc%2FReauwPts%2FQxNVVCGYD4QeCTHswcnzfi5L7k12N8kCIswpt%2Fy06Nt2p5mdYiwCDSwRFbm17Qv6UiB0b75U%2BGjNVQ7UZb14nkTF%2FcUINRI78%2Bx0JHrp%2BqRZhysjeVXEIUmiQraFQwyb3y%2FVbUszNT1NavFsUC8RTRAIEB5700Ly2v5tCSR4jebWYyf54D20E%2F23SWJ79nNzCt8tKGRrxm43MlaE8zaxYhQJ4NZ7%2BvkTF5DM61LWSvglx7K%2F96lYAyXfU4bPTSu1uujLu0gLg0Hk2DNc9akd2LyhGYQ5HeC%2B8hSTblvCGoH09skyEAdIL5ycGLdTLS4HE6bCj81IcSfvUklaKN499itBbJ0zYo%3D',
           }
        """
        dict = {
                '汽车':'https://api.1sapp.com/content/getListV2?qdata=MjFDNDM4RUMyOTQxMDdBNjE5MzZDOEIzRkRCQUY0OUEuY0dGeVlXMGZOV1ExWkRRMllUZ3RaV0psTmkwME4yWXhMVGxsWXpRdE5XSTFObU5rTlRaak1USmpIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGsuFv79cIPSRHGlYguUrPyb3j50grWMcRDl8zlgKwS6yLBCzALlCtHIanl52foD9zw9n4r%2FORuNxfjWcl4gkG0tAlD9B3%2BGeDuldv707HZkpQbUCbKbBpdqunqXakA8eZ38DJtV4hV8cULnZHp6%2BPinpshJbzvgfvcOIk5D0GWMohbDFDO4EKC1%2Fs%2BKOALMBEGSfKXrl4dG%2BiOE0xORbtKk%2BD3ZAxsWfS%2Bmy4IE1MKOtiC7KoxyJyC2GNLXNR9xZt7SCkt3V6a54gR%2B7McizTtgC91jqJG7LKhC4WA7zsAeTpDKkzNZfc7tCK9gFit5tvN5U00d5Ti5buWCW4%2FHIx0bf0%2BWOoYbRrnmXe8PCrIOv7%2FdDBpJ851P%2FSIyQ6wqjjWfjbr0mQXcOjmWXtY5Q3LtDdz7YOrJLRh%2B8IbB7%2BDyN1KFIrufGLB%2BB2uc%2FhRbZKdhUpCY48c8uxhA2PkbahNEKktsaVdo11blNGHZVOSwiHV7CWkeoUaNnHnwIGYFF7IKPgQ1j9viV7TQ0QvpeMKBeww%3D'
               }
        for key,value in dict.items():
            remark = key
            url = value
            url_type = 1
            try:
                print key
                text = self.getcontent(url,url_type)
                text = json.loads(text)
                datas = text['data']
                datas = datas['data']
                for data in datas:
                    if 'title' in data:
                        title = data['title']
                        url = data['url']
                        url = url.split('&key=')[0]
                        cover_pic = data['cover']
                        cover_pic = cover_pic[0]
                        self.gettime(title,url,cover_pic,remark)
            except:
                print('wrong')
    def gettime(self,title,url,cover_pic,remark):
        url_type = 1
        text = self.getcontent(url,url_type)
        scripts = etree.HTML(text).xpath('//script//text()')
        try:
            for script in scripts:
                if 'createTime' in script:
                    script = json.loads(script)
                    createTime = script['createTime']
                    video = script['video']
                    value = video['value']
                    nickname = script['nickname']
                    nickname_pic = script['avatar']
                    json_url = 'http://mpapi.qutoutiao.net/video/getAddressByFileId?file_id=' + str(value)
                    self.getvideo(title,cover_pic,createTime,json_url,nickname,nickname_pic,remark)
        except:
            print('wrong')
    def getvideo(self,title,cover_pic,createTime,json_url,nickname,nickname_pic,remark):
        url = json_url
        url_type = 1
        text = json.loads(self.getcontent(url,url_type))
        data = text['data']
        if 'definition' in data:
            hd = data['hd']
            video_url = hd['url']
            table = 'video'
            mapx = {}
            hash = hashlib.md5()
            hash.update(title.encode(encoding='utf-8'))
            newTitle = hash.hexdigest()
            mapx['title'] = title
            mapx['cover_pic'] = cover_pic
            mapx['create_time'] = createTime
            mapx['video_url'] = video_url
            mapx['video_info'] = nickname
            mapx['file_name'] = nickname_pic
            mapx['status'] = 5
            mapx['hash'] = newTitle
            mapx['ownner_id'] = 0
            mapx['video_address'] = 'qutoutiao' + '-' + remark
            result = self.select(newTitle)
            if int(result) == 1:
                print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + newTitle
                insertid = self.insert(table, mapx)
    def select(self,title):
        selecturl = 'https://apipre.xiaomatv.cn/V3/Article/checkVideo?title=' + title
        result = requests.get(selecturl).text
        return result
    def getcontent(self,url,url_type):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        }
        try:
            if url_type == 1:
                content = requests.get(url=url,headers = header,timeout = 3).content
                return content
        except:
            print('request wrong')
qutoutiaovideo = QuTouTiaoVideo()
qutoutiaovideo.getlinkurls()
print "休息5秒"
time.sleep(5)
qutoutiaovideo.getlinkurls()
print "休息10秒"
time.sleep(10)
qutoutiaovideo.getlinkurls()
print "休息15秒"
time.sleep(15)
qutoutiaovideo.getlinkurls()
print "休息20秒"
time.sleep(20)
qutoutiaovideo.getlinkurls()
print "休息25秒"
time.sleep(25)
qutoutiaovideo.getlinkurls()
print "休息30秒"
time.sleep(30)
qutoutiaovideo.getlinkurls()
print "休息35秒"
time.sleep(35)
qutoutiaovideo.getlinkurls()
print "休息40秒"
time.sleep(40)
qutoutiaovideo.getlinkurls()
print "休息45秒"
time.sleep(45)
qutoutiaovideo.getlinkurls()
print "休息50秒"
time.sleep(50)
qutoutiaovideo.getlinkurls()
print "休息55秒"
time.sleep(55)
qutoutiaovideo.getlinkurls()
print "休息60秒"
time.sleep(60)