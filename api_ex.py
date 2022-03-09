@app.post('/new_player', tags=['Main'], responses={200: {"model": StatusMessage}, 400: {"model": ErrorMessage}})
@transaction.atomic
def create_new_player(player: PlayerItem, Authorize: AuthJWT = Depends()):
    """
    Creates new player.
    """
    Authorize.jwt_required()
    v = Validator(alfa_range=('a', 'f'))

    with transaction.atomic():
        try:
            v.validate(name=player.name, email=player.email)
            try:
                v.db_exist_check(player.name, player.email, Player)
                new_player = Player()
                new_player.name = player.name
                new_player.email = player.email
                new_player.save()

                return JSONResponse(content={"status": "success", "id": new_player.id, "success": True})

            except Exception as e:
                return e
        except Exception as e:
            return e
