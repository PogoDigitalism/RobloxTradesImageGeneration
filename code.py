## code is not optimized

async def generate_offer_image(limited_id_list,total_value,image_template,image_sizeX,image_sizeY):
    background = Image.open(image_template)
    size = (image_sizeX, image_sizeY)
    background = background.resize(size, Image.Resampling.LANCZOS)

    offerlist = str(limited_id_list).replace("[", "").replace("]", "")
    async with aiohttp.ClientSession() as session:
        r = await session.get(url=f'https://thumbnails.roblox.com/v1/assets?assetIds={offerlist}&size=250x250&format=Png&isCircular=false')
        resp = await r.json()
      
        limited_id_list = list(map(str,limited_id_list))
        add_x = -1
        glob_idx = 0
        try:
            for idx, assetId in enumerate(limited_id_list,glob_idx):
                glob_idx += 1
                data = resp['data']
                for item_img_data in data:
                    if item_img_data['targetId'] == int(assetId):
                        imageUrl = item_img_data['imageUrl']
                        break
                image_data = await session.get(url=imageUrl)
                img = Image.open(BytesIO(await image_data.read()))

                add_x += 1
                background.paste(img, (125 + (add_x * 315), 75), img)
        except:
            image_data = await session.get(url='https://media.discordapp.net/attachments/1080342571869552690/1101901390663655484/dsfsdfsd.png')
            img = Image.open(BytesIO(await image_data.read()))
            for idx, assetId in enumerate(limited_id_list, glob_idx):
                add_x += 1
                background.paste(img, (125 + (add_x * 315), 75), img)
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype('segoeuib.ttf', 40)

        text = 'Calculated trade value:'
        textval = f'{total_value}'

        draw.text((450, 412), text, font=font, align="left", fill=(55, 100, 226, 255))
        draw.text((900, 412), textval, font=font, align="middle", fill=(255, 255, 255, 255))

        await session.close()
        with BytesIO() as image_binary:
            background.save(image_binary, 'PNG')
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename='black.png')
            return file
