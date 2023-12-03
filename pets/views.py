from rest_framework.views import APIView, Request, Response, status
from .serializers import PetSerializer
from .models import Pet
from groups.models import Group
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination

class PetView(APIView, PageNumberPagination):
    
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        group_data = serializer.validated_data.pop("group")
        trait_data_list = serializer.validated_data.pop("traits")
        
        new_traits = []
        for trait_data in trait_data_list:
            try:
                trait = Trait.objects.get(name__iexact=trait_data["name"])
                new_traits.append(trait)
            except Trait.DoesNotExist:
                new_trait = Trait.objects.create(**trait_data)
                new_traits.append(new_trait)
        
        try:
            group = Group.objects.get(scientific_name__exact=group_data["scientific_name"])
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)
        
        new_pet = Pet.objects.create(**serializer.validated_data, group=group)
        new_pet.traits.set(new_traits)
        
        serializer = PetSerializer(new_pet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)
        serializer_pet = PetSerializer(result_page, many=True)
        
        return self.get_paginated_response(serializer_pet.data)
    
    
    def get(self, request: Request) -> Response:
        trait = request.query_params.get("trait")

        if trait:
            pets = Pet.objects.filter(traits__name=trait)
        else:
            pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, request)
        pets_serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(pets_serializer.data)


class petIdView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND) 
        serializer_pet = PetSerializer(pet)
        return Response(serializer_pet.data)
    
    
    def patch(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        serializer_request = PetSerializer(pet, data=request.data, partial=True)
        if not serializer_request.is_valid():
            return Response(serializer_request.errors, status.HTTP_400_BAD_REQUEST)

        group_data = serializer_request.validated_data.pop("group", None)
        trait_data_list = serializer_request.validated_data.pop("traits", None)

        new_traits = []
        for trait_data in trait_data_list:
            try:
                trait = Trait.objects.get(name__iexact=trait_data["name"])
                new_traits.append(trait)
            except Trait.DoesNotExist:
                new_trait = Trait.objects.create(**trait_data)
                new_traits.append(new_trait)

        try:
            group = Group.objects.get(scientific_name__exact=group_data["scientific_name"])
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)

        pet.group = group

        pet.traits.set(new_traits)

        for key, value in serializer_request.validated_data.items():
            setattr(pet, key, value)

        pet.save()

        return Response(PetSerializer(pet).data)


    def delete(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
