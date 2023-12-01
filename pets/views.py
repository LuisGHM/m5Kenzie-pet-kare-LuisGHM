from rest_framework.views import APIView, Request, Response, status
from .serializers import PetSerializer
from .models import Pet
from groups.models import Group
from traits.models import Trait

class PetView(APIView):
    
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        group_data = serializer.validated_data.pop("group")
        trait_data_list = serializer.validated_data.pop("traits")
        
        new_traits = []
        for trait_data in trait_data_list:
            try:
                trait = Trait.objects.get(name__iexact=trait_data["name"].lower())
                new_traits.append(trait)
            except Trait.DoesNotExist:
                new_trait = Trait.objects.create(**trait_data.lower())
                new_traits.append(new_trait)
        
        try:
            group = Group.objects.get(scientific_name__iexact=group_data["scientific_name"])
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)
        
        new_pet = Pet.objects.create(**serializer.validated_data, group=group)
        new_pet.traits.set(new_traits)
        
        serializer = PetSerializer(new_pet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
