from django import forms

from Store.models import Product


class SearchForm(forms.Form):
    ANY = 'AN'
    TECHNOLOGY = 'TE'
    FOOD = 'FO'
    CLOTHING = 'Cl'
    OTHER = 'OT'
    CATEGORY = [
        (ANY, 'Any'),
        (TECHNOLOGY, 'Technology'),
        (FOOD, 'Food'),
        (CLOTHING, 'Clothing'),
        (OTHER, 'Other'),
    ]
    PRICE_ANY = '0'
    PRICE_UNDER_10 = '1'
    PRICE_10_TO_30 = '2'
    PRICE_30_TO_70 = '3'
    PRICE_70_TO_150 = '4'
    PRICE_ABOVE_150 = '5'
    PRICE = [
        (PRICE_ANY, 'Any'),
        (PRICE_UNDER_10, 'Until The 10'),
        (PRICE_10_TO_30, '10 to 30'),
        (PRICE_30_TO_70, '30 to 70'),
        (PRICE_70_TO_150, '70 to 150'),
        (PRICE_ABOVE_150, 'Above 150')
    ]
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'searchTerm',
                                                                         'placeholder': 'Search product'}))
    category = forms.ChoiceField(label='Category', choices=CATEGORY, required=False, widget=forms.Select())
    price = forms.ChoiceField(label='price', choices=PRICE, required=False, widget=forms.Select(
        attrs={'transform': 'translate(350%, -750%)'}))

    def get_price(self):
        price_level = self.cleaned_data['price']
        if price_level == SearchForm.PRICE_UNDER_10:
            return None, 10
        elif price_level == SearchForm.PRICE_10_TO_30:
            return 10, 30
        elif price_level == SearchForm.PRICE_30_TO_70:
            return 30, 70
        elif price_level == SearchForm.PRICE_70_TO_150:
            return 70, 150
        elif price_level == SearchForm.PRICE_ABOVE_150:
            return 150, None
        else:
            return None, None
