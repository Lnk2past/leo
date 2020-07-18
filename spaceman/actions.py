                result = cnx.run(inputs.command)
                logger.info(result.stdout)
                if not result.ok:
                    logger.error(result.stderr)
