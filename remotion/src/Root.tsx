import { Composition } from 'remotion';
import { ViralComposition } from './ViralComposition';

export const RemotionRoot: React.FC = () => {
    return (
        <>
            <Composition
                id="ViralVideo"
                component={ViralComposition}
                durationInFrames={30 * 30} // 30 seconds
                fps={30}
                width={1080}
                height={1920}
                defaultProps={{}}
            />
        </>
    );
};

